__author__ = "Nicu Pavel <npavel@linuxconsulting.ro>"

import math
import random
import time
from evalfuncs import *

class HillClimbing:
    def __init__(self):
        self._nrbits = 10
        self._allbits = 20
        self._start = 0
        self._end = 0
        self._axes = 2
        self._decimals = 2
        self.eval = EvalFunc()


    def set_eval_function(self, EvalFunc):
        self.eval = EvalFunc()
        self._start = self.eval.start
        self._end = self.eval.end
        self._decimals = self.eval.decimals
        self._axes = self.eval.axes
        self._nrbits = self.get_nrbits()
        self._allbits = self._nrbits * self._axes

        print("Function %s" % self.eval.info())

    def modify_params(self, start = None, end = None, axes = None, decimals = None):
        if start is not None:
            self._start = start
        if end is not None:
            self._end = end
        if axes is not None:
            self._axes = axes
        if decimals is not None:
            self._decimals = decimals

        self._nrbits = self.get_nrbits()
        self._allbits = self._nrbits * self._axes

    def get_nrbits(self):
        return int(math.ceil(math.log((self._end - self._start) * math.pow(10, self._decimals), 2)))


    def generate_random_bits(self):
        return self.to_fixed_binary(random.getrandbits(self._allbits), self._allbits)


    def to_fixed_binary(self, n, nrbits):
        return bin(n)[2:].zfill(nrbits)


    def generate_all_neighbors(self, bitstr):
        neighbors = []
        n = int(bitstr, 2)
        for i in range(0, len(bitstr)):
            neighbors.append(self.to_fixed_binary(self.change_bit(n, i), self._allbits))

        return neighbors


    def to_float_in_interval(self, bitstr):
        l = []
        for i in range(0, len(bitstr), self._nrbits):
            n = int(bitstr[i:i + self._nrbits], 2)
            l.append(float(n) / (2 ** self._nrbits) * (self._end - self._start) + self._start)
        return l


    def change_bit(self, n, index):
        m = 1 << index
        return n ^ m


    def run(self, iterations=100):
        start = time.time()
        best_node  = self.generate_random_bits()
        best_node_float = self.to_float_in_interval(best_node)
        best_eval = self.eval.eval(best_node_float)

        print("Interval [%f %f] max bits: %d Random Node: %s" % (self._start, self._end, self._nrbits, best_node_float))
        for iteration in range(0, iterations):
            current_node  = self.generate_random_bits()
            current_node_float = self.to_float_in_interval(current_node)
            current_eval = self.eval.eval(current_node_float)
            neighbors = self.generate_all_neighbors(current_node)
            neighbors_float = [self.to_float_in_interval(x) for x in neighbors]

            #print("[%d] Current Node %s %s Eval %0.2f" %
            #    (iteration, map(float2e, current_node_float), current_node, current_eval))

            swapping = True
            while swapping:
                swapping = False
                neighbor = 0
                while neighbor < self._allbits:
                    x_float = neighbors_float[neighbor]
                    x_bits = neighbors[neighbor]  # the bit representation
                    x_eval = self.eval.eval(x_float)


                    #print("\t Neighbor %s %s Eval: %0.2f Local Best: %0.2f" %
                    #      (map(float2e, x_float),  x_bits, x_eval, current_eval))

                    if x_eval < current_eval:
                        current_node = x_bits
                        current_node_float = x_float
                        current_eval = x_eval
                        neighbors = self.generate_all_neighbors(current_node)
                        neighbors_float = [self.to_float_in_interval(x) for x in neighbors]
                        neighbor = 0
                        swapping = True
                        #print("\t - New Local Best %s %s" % (current_node_float, current_eval))

                    neighbor += 1

            if best_eval > current_eval:
                best_node = current_node
                best_node_float = current_node_float
                best_eval = current_eval
                print("[%d]* New Global Best: %0.2f  %s"
                      % (iteration, best_eval, map(float2e, best_node_float)))

        end = time.time()
        print("Finished %d iterations in %0.3f seconds ! \n"
              " Global Best: %0.2f %s" % (iterations, (end - start ), best_eval, map(float2e, best_node_float)))
        return best_node_float


if __name__ == "__main__":
    #test(5, 2, -5.12, 5.12)
    hillclimb = HillClimbing()

    hillclimb.set_eval_function(Rastrigin)
    hillclimb.run(iterations=300)

    hillclimb.set_eval_function(Griewangk)
    hillclimb.run(iterations=300)

    hillclimb.set_eval_function(Rosenbrock)
    hillclimb.run(iterations=300)

    hillclimb.set_eval_function(Sixhump)
    hillclimb.run(iterations=300)
