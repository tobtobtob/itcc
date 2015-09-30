'''DEAP example. We try to evolve a list of digits to match a target list of 
digits, that represents a date.
'''
import random
from deap import algorithms
from deap import base
from deap import creator
from deap import tools

# Date, a target which we want to evolve. 
target = [2, 4, 0, 9, 2, 0, 1, 5]

# Our evaluation function
def eval(individual):
    '''Evaluate individual. 
    
    The closer the individual is to the target, the better the fitness.
    '''
    fit = 0
    for i in xrange(len(individual)):
        if i % 2 == 0:
            fit = fit + individual[i]
        else:
            fit = fit + (1-individual[i])
    
    # Evaluation function has to return a tuple, even if there is only one
    # evaluation criterion (thats why there is a comma).    
    return fit, 

# We create a fitness for the individuals, because our eval-function gives us 
# "better" values the closer they are zero, we will give it weight -1.0.
# This creates a class creator.FitnessMin(), that is from now on callable in the
# code. (Think about Java's factories, etc.)
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))

# We create a class Individual, which has base type of list, it also uses our 
# just created creator.FitnessMin() class.
creator.create("Individual", list, fitness=creator.FitnessMin)

# We create DEAP's toolbox. Which will contain our mutation functions, etc.
toolbox = base.Toolbox()

# We create a function named 'random_digit', which calls random.randint 
# with fixed parameters, i.e. calling toolbox.random_digit() is the same as 
# calling random.randint(0, 9)
toolbox.register('random_digit', random.randint, 0, 1)

# Now, we can make our individual (genotype) creation code. Here we make the function to create one instance of 
# creator.Individual (which has base type list), with tools.initRepeat function. tool.initRepeat 
# calls our just created toolbox.random_digit function n-times, where n is the 
# length of our target. This is about the same as: [random.randint(0,9) for i in xrange(len(target))].
# However, our created individual will also have fitness class attached to it (and 
# possibly other things not covered in this example.)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.random_digit, n = 400)

# As we now have our individual creation code, we can create our population code
# by making a list of toolbox.individual (which we just created in last line).
# Here it is good to know, that n (population size), is not defined at this time 
# (but is needed by the initRepeat-function), and can be altered when calling the 
# toolbox.population. This can be achieved by something called partial functions, check 
# https://docs.python.org/2/library/functools.html#functools.partial if interested.
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# We register our evaluation function, which is now callable as toolbox.eval(individual).
toolbox.register("evaluate", eval)

# We use simple selection strategy where we select only the best individuals, 
# now callable in toolbox.select.
toolbox.register("select", tools.selBest)

# We use one point crossover, now callable in toolbox.mate.
toolbox.register("mate", tools.cxOnePoint)

# We define our own mutation function which replaces one index of an individual
# with random digit.
def mutate(individual):
    for i in range(len(individual)):
        bit = random.random()
        if bit < 0.05:
            individual[i] = 1 - individual[i]
    return individual,

def crossover(ind1, ind2):
    temp = list(ind1)
    point = random.randint(0, len(ind1)-1)
    for i in range(point, len(ind1)-1):
        ind1[i] = ind2[i]
        ind2[i] = temp[i]
    return ind1, ind2
                   

# We register our own mutation function as toolbox.mutate
toolbox.register("mutate", mutate)
toolbox.register("crossover", crossover)

# Now we have defined basic functions with which the evolution algorithm (EA) can run.
# Next, we will define some parameters that can be changed between the EA runs.

# Maximum amount of generations for this run
generations = 100

# Create population of size 100 (Now we define n, which was missing when we 
# registered toolbox.population).
pop = toolbox.population(n=100)

# Create hall of fame which stores only the best individual
hof = tools.HallOfFame(1)

# Get some statistics of the evolution at run time. These will be printed to
# sys.stdout when the algorithm is running.
import numpy as np
stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("avg", np.mean)
stats.register("std", np.std)
stats.register("min", np.min)
stats.register("max", np.max)

# Probability for crossover
crossover_prob = 0.7

# Probability for mutation
mutation_prob = 0.1

# Call our actual evolutionary algorithm that runs the evolution.
# eaSimple needs toolbox to have 'evaluate', 'select', 'mate' and 'mutate'
# functions defined. This is the most basic evolutionary algorithm. Here, we 
# have crossover probability of 0.7, and mutation probability 0.2.
algorithms.eaSimple(pop, toolbox, crossover_prob, mutation_prob, generations, stats, halloffame=hof)

# Print the best individual, and its fitness
print hof[0], eval(hof[0])

import numpy as np
ar = np.asarray(hof[0])
img = ar.reshape((20,20))
img[img == 1] = 255 # change each 1 to 255 
from skimage import io
io.imsave('ga_array.png', img)
