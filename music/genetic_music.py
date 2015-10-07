'''DEAP example. We try to evolve a list of digits to match a target list of 
digits, that represents a date.
'''
import random
from deap import algorithms
from deap import base
from deap import creator
from deap import tools


execfile('music_chains.py')

filename = "notes.txt"

notes = open(filename, 'r').read().split()

def extract_pitch(notes):
	return map(lambda y : filter(lambda x: x not in (map(str, range(10))+['.']), y), notes)

only_pitch = extract_pitch(notes)

last_time = str(4)
def time_or_last_time(string):
    ret = filter(lambda x: x in map(str, range(10)), string)
    global last_time
    if ret == "":
        return last_time
    last_time = ret
    return ret

def extract_time(notes):
	return map(time_or_last_time, notes)

only_time = extract_time(notes)
pitch_chain = create(only_pitch, 3)
time_chain = create(only_time, 3)

smoothing = lambda x: x+2

smooth(pitch_chain.chain, smoothing)
smooth(time_chain.chain, smoothing)


# Our evaluation function

def eval(individual):
	pitches = extract_pitch(individual)
	#time = extract_time(individual)
	return pitch_chain.evaluate(pitches),

# We create a fitness for the individuals, because our eval-function gives us 
# "better" values the closer they are zero, we will give it weight -1.0.
# This creates a class creator.FitnessMin(), that is from now on callable in the
# code. (Think about Java's factories, etc.)
creator.create("FitnessMin", base.Fitness, weights=(1.0,))

# We create a class Individual, which has base type of list, it also uses our 
# just created creator.FitnessMin() class.
creator.create("Individual", list, fitness=creator.FitnessMin)

# We create DEAP's toolbox. Which will contain our mutation functions, etc.
toolbox = base.Toolbox()



all_notes = list(set(extract_pitch(notes)))
def random_note():
	return all_notes[random.randint(0,len(all_notes)-1)]
	
toolbox.register('random_note', random_note)

# Now, we can make our individual (genotype) creation code. Here we make the function to create one instance of 
# creator.Individual (which has base type list), with tools.initRepeat function. tool.initRepeat 
# calls our just created toolbox.random_digit function n-times, where n is the 
# length of our target. This is about the same as: [random.randint(0,9) for i in xrange(len(target))].
# However, our created individual will also have fitness class attached to it (and 
# possibly other things not covered in this example.)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.random_note, n = 50)

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
    i = random.randint(0, len(individual)-1)
    individual[i] = toolbox.random_note()
    # DEAP's mutation function has to return a tuple, thats why there is comma
    # after. 
    return individual,

# We register our own mutation function as toolbox.mutate
toolbox.register("mutate", mutate)

# Now we have defined basic functions with which the evolution algorithm (EA) can run.
# Next, we will define some parameters that can be changed between the EA runs.

# Maximum amount of generations for this run
generations = 50

# Create population of size 100 (Now we define n, which was missing when we 
# registered toolbox.population).
pop = toolbox.population(n=10000)

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

result = hof[0]
result[0] =result[0]+'8'

score_start = "\\version \"2.18.2\"\n\score {\n<<\n{ \key c \major\n"
score_end = "\n}     \n>>\n\midi { }\n\layout { }\n}"

result = score_start + ' '.join(result) + score_end
f = open("genetic_score.ly", 'w')
f.write(result)
f.close()

