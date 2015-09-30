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


pset = gp.PrimitiveSet("pset", 1)

pset.addPrimitive(operator.and_, 2)
pset.addPrimitive(operator.or_, 2)
pset.addPrimitive(operator.not_, 1)
pset.addPrimitive(operator.xor, 2)

pset.addEphemeralConstant("rand1",lambda: random.randint(0,1))
pset.addEphemeralConstant("rand2",lambda: random.randint(0,1))

target = time.time()


listlength = 400

def evaluate(individual):
	func = toolbox.compile(individual)
	test = list(range(listlength))
	test = map(func, test)
	fit = 0
	for i in xrange(listlength):
		if i % 3 == 0:
			fit = fit + abs(1-test[i])
		else:
			fit = fit + test[i]
       
	return fit, 

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
generations = 500
pop = algorithms.eaSimple(pop, toolbox, mateprob, mutprob, generations, halloffame=hof, verbose=False)

def show(tree):
	ret = list(range(listlength))
	return map(toolbox.compile(tree), ret)

print evaluate(hof[0])
print show(hof[0])
