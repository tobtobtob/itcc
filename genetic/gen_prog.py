from deap import gp
from deap import creator
from deap import base
from deap import tools
from deap import algorithms

import operator
import random
import time

def protectedDiv(left, right):
    try:
        return left / right
    except ZeroDivisionError:
        return 1


pset = gp.PrimitiveSet("pset", 0)
pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.sub, 2)
pset.addPrimitive(operator.mul, 2)
pset.addPrimitive(protectedDiv, 2)
pset.addPrimitive(operator.abs, 1)
pset.addEphemeralConstant("rand1",lambda: random.randint(0,5))
pset.addEphemeralConstant("rand2",lambda: random.randint(0,5))

target = time.time()

def evaluate(individual):
	val = toolbox.compile(expr = individual)
	return int(abs(val-target)),


creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("evaluate", evaluate)
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)
toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))

random.seed(time.time())
pop = toolbox.population(n=100)
hof = tools.HallOfFame(1)
mateprob = 0.1
mutprob = 0.5
generations = 100
pop = algorithms.eaSimple(pop, toolbox, mateprob, mutprob, generations, halloffame=hof, verbose=False)

print evaluate(hof[0])
