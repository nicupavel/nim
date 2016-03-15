#!/usr/bin/python

import math
import random
import time
import copy
from evalfuncs import *

class ChangeProbabilities:
    def __init__(self):
        self.mutation = 0.5
        self.crossover = 0.4
        self.hybrid = 0.3


class Chromosome(object):
    def __init__(self, components=2, decimals=3, eval = EvalFunc):
        self.components = components
        self.decimals = decimals
        self.eval = eval()
        self.func = eval

        self.bitsPerComponent = []
        self.bitsTotal = 0
        self.bits = 0
        self.floats = []
        self.value = None
        self.fitness = None

        #print "Using function: %s" % self.eval.info()

        self.__getBitRepresentation()
        self.bits = Chromosome.generateRandomBits(self.bitsTotal)

        #print "Bits per component:", self.bitsPerComponent
        #print "Total bits: %d" % self.bitsTotal
        #print "Random bits: %s" % self.bits


    def updateValues(self):
        self.asFloatInInterval()
        self.value = self.eval.eval(self.floats)
        self.fitness = self.eval.fitness(self.floats)


    def crossoverOnepoint(self, other):
        pos = random.randint(1, self.bitsTotal)
        #print "Crossed One Point %d\n\t%s\t%s" % (pos, self.bits, other.bits)
        thisRight = self.bits[pos:self.bitsTotal]
        otherRight = other.bits[pos:other.bitsTotal]
        self.bits = self.bits[:pos] + otherRight
        other.bits = other.bits[:pos] + thisRight
        #print "\t%s\t%s" % (self.bits, other.bits)


    def mutate(self, probability=0.5):
        #print "Mutated\n\t %s" % self.bits
        for i in range(0, self.bitsTotal):
            if random.random() > probability:
                if self.bits[i] == '1':
                    newBit = '0'
                else:
                    newBit = '1'

                self.bits = self.bits[:i] + newBit + self.bits[i+1:]
        #print "\t %s" % self.bits


    def hybrid(self):
        return self.hybridHillclimb()

    def hybridHillclimb(self):
        neighbors = self.generateAllNeighbors()
        c = copy.deepcopy(self)
        best = copy.deepcopy(self)
        #print "Initial Hillclimb: ",
        #c.dump()
        for n in neighbors:
            c.bits = n
            c.updateValues()
            #print "* Neighbor %s fitness: %0.2f local: %0.2f best:%0.2f" % (n, c.fitness, self.fitness, best.fitness)
            #c.dump()
            if c.fitness > self.fitness and c.fitness > best.fitness:
                    #print "\tBetter fitness %f > %f" % (c.fitness, best.fitness)
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
        print("%s %s Value: %0.2f Fitness: %0.4f" % (self.bits, map(float2e, self.floats), self.value, self.fitness))


    def __getBitRepresentation(self):
        for i in self.eval.intervals:
            l = self.getNrBits(i[0], i[1], self.decimals)
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

    def __init__(self, size=100, components=2, decimals=3, eval = EvalFunc, elitism = 1, changeProb = ChangeProbabilities()):
        self.size = size
        self.components = components
        self.decimals = decimals
        self.eval = eval
        self.changeProb = changeProb
        self.elitism = elitism
        self.population = []
        self.best = None
        self.unchangedSteps = 0

    def generatePopulation(self):
        print "Generating Population with size %d" % self.size
        for i in range(0, self.size):
            c = Chromosome(self.components, self.decimals, self.eval)
            c.updateValues()
            #c.dump()
            self.population.append(c)
        self.sortByFitness()

    def crossover(self, shouldUpdate = True):
        selection = []
        for c in self.population[self.elitism:]:
            if random.random() > self.changeProb.crossover:
                selection.append(c)

        slen = len(selection)
        it = iter(selection)
        print "Selected %d for crossover" % slen

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
            if random.random() > self.changeProb.hybrid:
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

        for i in range(0, len(self.population)):
            sumFitness = 0.0
            r = random.uniform(0, sumFitnessTotal)
            #print "Selection %d %0.3f/%0.3f" % (i, r, sumFitnessTotal)
            for c in self.population:
                sumFitness += c.fitness
                if sumFitness >= r:
                    newPopulation.append(copy.deepcopy(c))
                    break

        self.population = newPopulation


    def step(self):
        self.selection()
        self.crossover(shouldUpdate=False)
        self.mutate(shouldUpdate=False)
        self.hybrid(shouldUpdate=False)
        self.updateValues()

        currentBest = self.population[0]
        if self.best is None or self.best.fitness < currentBest.fitness:
            print "Top chromosome: ",
            self.best = currentBest
            self.best.dump()
        else:
            print "Not improved in this step"
            self.unchangedSteps += 1



    def dump(self):
        print '-' * 80
        for c in self.population:
            c.dump()
        print '-' * 80

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

    #print c1.generateAllNeighbors()

    #c1.hybridHillclimb()
    #p = Population(100, 2, 3, Rastrigin)
    p = Population(10, 2, 3, Sixhump)
    p.generatePopulation()
    p.dump()

    # p.crossover()
    # p.dump()
    # p.mutate()
    # p.dump()
    # p.hybrid()
    # p.dump()
    # p.selection()
    # print "After Selection"
    # p.dump()
    # p.step()

    maxUnchangedSteps = 10
    for i in range(0, 200):
        p.step()
        p.dump()
        if p.unchangedSteps > maxUnchangedSteps:
            print "Unchanged in %d steps. Finishing." % maxUnchangedSteps
            break

    print "Best: ", p.best.dump()
