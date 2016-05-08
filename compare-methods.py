import random
import copy
from ga import *
from pso import *
from evalfuncs import *
import numpy

GA_POP_SIZE = 40
RUNS = 30

def getMean(l):
    arr = numpy.array(l)
    return numpy.mean(arr, axis=0)

def getStdDev(l):
    arr = numpy.array(l)
    return numpy.std(arr, axis=0)

def runGA(function = Rastrigin, dimensions = 2, useHybridization = False):
    values = []
    if useHybridization:
        prob = ProbabilitiesWithHybridization
    else:
        prob = ProbabilitiesNoHybridization

    for run in range(0, RUNS):
        EvaluationOverflow.current = 0
        p = Population(size=GA_POP_SIZE, eval=function, changeProb=prob())
        p.generatePopulation()
        for i in range(0, 10000):
            try:
                p.step()
                #p.dumpBest()
            except EvaluationOverflow:
                log.info("Evaluation limit reached !")
                break
        values.append(p.best.value)
    return values

valuesGA = runGA(useHybridization=False)
valuesGAHybrid = runGA(useHybridization=True)

print valuesGA
print valuesGAHybrid

print("Normal GA: Mean: %.2f StdDev: %.2f" % (getMean(valuesGA), getStdDev(valuesGA)))
print("Hybrid GA: Mean: %.2f StdDev: %.2f" % (getMean(valuesGAHybrid), getStdDev(valuesGAHybrid)))