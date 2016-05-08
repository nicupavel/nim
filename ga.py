#!/usr/bin/python

import math
import random
import time
import copy
from log import log
from evalfuncs import *

class ProbabilitiesWithHybridization:
    def __init__(self):
        self.mutation = 0.01
        self.crossover = 0.4
        self.hybrid = 0.5

class ProbabilitiesNoHybridization:
    def __init__(self):
        self.mutation = 0.01
        self.crossover = 0.4
        self.hybrid = -1

class Chromosome(object):
    def __init__(self, eval = EvalFunc):
        self.eval = eval

        self.bitsPerComponent = []
        self.bitsTotal = 0
        self.bits = 0
        self.floats = []
        self.value = None
        self.fitness = None

        log.debug("Using function: %s" % self.eval.info())

        self.__getBitRepresentation()
        self.bits = Chromosome.generateRandomBits(self.bitsTotal)

        log.debug("Bits per component:", self.bitsPerComponent)
        log.debug("Total bits: %d" % self.bitsTotal)
        log.debug("Random bits: %s" % self.bits)


    def updateValues(self):
        EvaluationOverflow.check()
        self.asFloatInInterval()
        self.value = self.eval.eval(self.floats)
        self.fitness = self.eval.fitness(self.floats)


    def crossoverOnepoint(self, other):
        pos = random.randint(1, self.bitsTotal)
        #log.debug("Crossed One Point %d\n\t%s\t%s" % (pos, self.bits, other.bits))
        thisRight = self.bits[pos:self.bitsTotal]
        otherRight = other.bits[pos:other.bitsTotal]
        self.bits = self.bits[:pos] + otherRight
        other.bits = other.bits[:pos] + thisRight
        #log.debug("\t%s\t%s" % (self.bits, other.bits))


    def mutate(self, probability=0.5):
        #log.debug "Mutated\n\t %s" % self.bits
        for i in range(0, self.bitsTotal):
            if random.random() < probability:
                if self.bits[i] == '1':
                    newBit = '0'
                else:
                    newBit = '1'

                self.bits = self.bits[:i] + newBit + self.bits[i+1:]
        #log.debug("\t %s" % self.bits)

    def hybrid(self):
        return self.hybridHillclimb()

    def hybridHillclimb(self):
        neighbors = self.generateAllNeighbors()
        c = copy.deepcopy(self)
        best = copy.deepcopy(self)
        #log.debug("Initial Hillclimb: ")
        #log.debug(c.dump())
        for n in neighbors:
            c.bits = n
            c.updateValues()
            #log.debug "* Neighbor %s fitness: %0.2f local: %0.2f best:%0.2f" % (n, c.fitness, self.fitness, best.fitness)
            #c.dump()
            if c.fitness > self.fitness and c.fitness > best.fitness:
                log.debug("\tHybridization: Better fitness %f > %f" % (c.fitness, best.fitness))
                best = copy.deepcopy(c)
        self.bits = best.bits
        self.updateValues()

    def asFloatInInterval(self):
        p = 0
        i = 0
        self.floats = []
        while i < self.bitsTotal:
            nrbits = self.bitsPerComponent[p]
            start = self.eval.intervals[p][0]
            end = self.eval.intervals[p][1]
            n = int(self.bits[i:i + nrbits], 2)

            self.floats.append(float(n) / (2 ** nrbits) * (end - start) + start)
            i += nrbits
            p += 1

    def dump(self):
        log.info("%s %s Value: %0.2f Fitness: %0.4f" % (self.bits, map(float2e, self.floats), self.value, self.fitness))


    def __getBitRepresentation(self):
        for i in self.eval.intervals:
            l = Chromosome.getNrBits(i[0], i[1], self.eval.decimals)
            self.bitsPerComponent.append(l)
            self.bitsTotal += l

    def generateAllNeighbors(self):
        neighbors = []
        n = int(self.bits, 2)
        for i in range(0, len(self.bits)):
            neighbors.append(Chromosome.asBinary(Chromosome.changeBit(n, i), self.bitsTotal))

        return neighbors

    @staticmethod
    def changeBit(n, index):
        m = 1 << index
        return n ^ m

    @staticmethod
    def generateRandomBits(nrbits):
        return Chromosome.asBinary(random.getrandbits(nrbits), nrbits)

    @staticmethod
    def getNrBits(start, end, decimals):
        return int(math.ceil(math.log((end - start) * math.pow(10, decimals), 2)))

    @staticmethod
    def asBinary(n, nrbits):
        return bin(n)[2:].zfill(nrbits)



class Population(object):

    def __init__(self, size=100, eval = EvalFunc, elitism = 1, changeProb = ProbabilitiesNoHybridization()):
        self.size = size
        self.eval = eval()
        self.changeProb = changeProb
        self.elitism = elitism
        self.population = []
        self.best = None
        self.unchangedSteps = 0
        log.info(self.eval.info())

    def generatePopulation(self):
        log.debug("Generating Population with size %d" % self.size)
        for i in range(0, self.size):
            c = Chromosome(self.eval)
            c.updateValues()
            #c.dump()
            self.population.append(c)
        self.sortByFitness()

    def crossover(self, shouldUpdate = True):
        selection = []
        for c in self.population[self.elitism:]:
            if random.random() < self.changeProb.crossover:
                selection.append(c)

        slen = len(selection)
        it = iter(selection)
        log.debug("Selected %d for crossover" % slen)

        for c in it:
            try:
                c.crossoverOnepoint(next(it))
            except Exception, e:
                break

        if shouldUpdate:
            self.updateValues()

    def mutate(self, shouldUpdate = True):
        for c in self.population[self.elitism:]:
            c.mutate(self.changeProb.mutation)

        if shouldUpdate:
            self.updateValues()

    def hybrid(self, shouldUpdate = True):
        for c in self.population[self.elitism:]:
            if random.random() < self.changeProb.hybrid:
                c.hybrid()

        if shouldUpdate:
            self.updateValues()


    def selection(self):
        return self.rouletteSelection()


    def rouletteSelection(self):
        newPopulation = []
        sumFitnessTotal = 0.0
        for c in self.population:
            sumFitnessTotal += c.fitness
        log.debug("* Total Fitness %0.3f" % sumFitnessTotal)

        for i in range(0, len(self.population)):
            sumFitness = 0.0
            r = random.uniform(0, sumFitnessTotal)
            #log.debug "Selection %d %0.3f/%0.3f" % (i, r, sumFitnessTotal)
            for c in self.population:
                sumFitness += c.fitness
                if sumFitness >= r:
                    newPopulation.append(copy.deepcopy(c))
                    break

        self.population = newPopulation


    def step(self):
        self.selection()

        sumFitnessTotal = 0.0
        for c in self.population:
            sumFitnessTotal += c.fitness
        self.updateValues()

        log.debug("* Total Fitness After selection %0.3f" % sumFitnessTotal)

        self.crossover(shouldUpdate=False)
        self.mutate(shouldUpdate=False)
        self.hybrid(shouldUpdate=False)
        self.updateValues()

        currentBest = self.population[0]
        if self.best is None or self.best.fitness < currentBest.fitness:
            log.debug("Top chromosome: ")
            self.best = currentBest
            self.best.dump()
        else:
            log.debug("Not improved in this step")
            self.unchangedSteps += 1


    def dumpBest(self):
        self.population[0].dump()

    def dump(self):
        log.info('-' * 80)
        for c in self.population:
            c.dump()
        log.info('-' * 80)

    def sortByFitness(self):
        self.population.sort(key = lambda c: c.fitness, reverse = True)

    def updateValues(self, shouldSort = True):
        for c in self.population:
            c.updateValues()

        if shouldSort:
            self.sortByFitness()



if __name__ == "__main__":
    # c1 = Chromosome(2, 3, Rastrigin)
    # c2 = Chromosome(2, 3, Rastrigin)
    # c1.updateValues()
    # c2.updateValues()
    # c1.dump()
    # c2.dump()
    #
    # c1.mutate()
    # c1.crossoverOnepoint(c2)

    #log.debug c1.generateAllNeighbors()

    #c1.hybridHillclimb()
    #p = Population(50, 30, 2, Rastrigin)

    #p = Population(10, 2, 3, Sixhump)


    # p.crossover()
    # p.dump()
    # p.mutate()
    # p.dump()
    # p.hybrid()
    # p.dump()
    # p.selection()
    # log.debug "After Selection"
    # p.dump()
    # p.step()

    runSimulation = True
    runBasinSimulation = False
    maxUnchangedSteps = None

    if runSimulation:
        p = Population(size=50, eval=Rastrigin, changeProb=ProbabilitiesNoHybridization())
        p.generatePopulation()
        p.dump()
        for i in range(0, 40):
            try:
                p.step()
                p.dumpBest()
            except EvaluationOverflow:
                log.info("Evaluation limit reached !")
                break

            if maxUnchangedSteps is not None and p.unchangedSteps > maxUnchangedSteps:
                log.debug("Unchanged in %d steps. Finishing." % maxUnchangedSteps)
                break

        log.info("Best: ")
        p.best.dump()

    if runBasinSimulation:
        result = {}
        for i in range(0, 32):
            c = Chromosome(1, 0, Miscfunc1)
            c.updateValues()
            #c.dump()
            c.hybridHillclimb()
            b = int(c.floats[0])
            if result.get(b, None) is None:
                result[b] = [i]
            else:
                result[b].append(i)

        from pprint import pprint
        pprint(result)
