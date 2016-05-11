import random
import copy
from ga import *
from pso import *
from evalfuncs import *
import numpy
import time

GA_POP_SIZE = 100
RUNS = 30

def getMean(l):
    arr = numpy.array(l, dtype=numpy.float)
    return numpy.nanmean(arr, axis=0)

def getStdDev(l):
    arr = numpy.array(l, dtype=numpy.float)
    return numpy.nanstd(arr, axis=0)

def runGA(function = Rastrigin(axes=2), useHybridization = False):
    values = []
    if useHybridization:
        prob = ProbabilitiesWithHybridization
    else:
        prob = ProbabilitiesNoHybridization

    log.info("Running for %s with %d axes hybridization: %s" % (function.info(), function.axes, useHybridization))

    for run in range(0, RUNS):
        EvaluationOverflow.current = 0
        #print("Run %d/%d" % (run, RUNS))
        p = Population(size=GA_POP_SIZE, eval=function, changeProb=prob())
        p.generatePopulation()
        for i in range(0, 100000):
            try:
                p.step()
                #p.dumpBest()
            except EvaluationOverflow:
                log.debug("Evaluation limit reached !")
                break

        if p.best is not None:
            values.append(p.best.value)
    return values


def runPSO(function = Rastrigin(axes=2)):
    values = []
    w1 = 0.7  # inertia
    w2 = 1.6  # cognitive
    w3 = 1.5  # social

    maxParticles = 200
    maxIterations = 10000 # ignored by PSO when number of evaluations is enabled

    log.info("Running for %s with %d axes" % (function.info(), function.axes))

    for run in range(0, RUNS):
        EvaluationOverflow.current = 0
        #print("Run %d/%d" % (run, RUNS))
        best = PSO(maxIterations, maxParticles, function, function.start, function.end, w1, w2, w3)
        if best is not None:
            values.append(function.eval(best))

    return values


def runAllTests():
    funcs = (Rastrigin, Griewangk, Rosenbrock, Sixhump)
    axes = (5, 10, 30)

    #funcs = (Rastrigin,)
    #axes = (2,)

    results = {}

    # GA
    for f in funcs:
        for a in axes:
            for t in [False, True]:
                name = "GA-" + str(f) + "-" + str(a)+ "-" + str(t)
                results[name] = runGA(function=f(axes=a), useHybridization=t)
                results[name+"-mean"] = getMean(results[name])
                results[name+"-std"] = getStdDev(results[name])
                print("Done:", name)

    # PSO
    for f in funcs:
        for a in axes:
            name = "PSO-" + str(f) + "-" + str(a)
            results[name] = runPSO(function=f(axes=a))
            results[name+"-mean"] = getMean(results[name])
            results[name+"-std"] = getStdDev(results[name])
            print("Done:", name)

    numpy.save("results-" + str(EvaluationOverflow.limit) + "-runs-" + str(int(time.time())), results)


if __name__ == "__main__":
    start = int(time.time())
    runAllTests()
    end = int(time.time())
    print time.strftime('%H:%M:%S', time.gmtime(end - start))