__author__ = "Nicu Pavel <npavel@linuxconsulting.ro>"

import math
import random
import time
from evalfuncs import *


def get_nrbits(start, end, q):
    return int(math.ceil(math.log((end - start) * math.pow(10, q), 2)))


def generate_random_bits(nrbits):
    return random.getrandbits(nrbits)


def to_bit_list(intlist, nrbits=7):
    b = []
    for n in intlist:
        b.append(to_fixed_binary(n, nrbits))
    return b


def to_fixed_binary(n, nrbits=7):
    return bin(n)[2:].zfill(nrbits)


def generate_all_neighbors(list, nrbits=7):
    neighbors = []
    for n in list:
        current_neighbors = []
        for i in range(0, nrbits):
            current_neighbors.append(change_bit(n, i))
        neighbors.append(current_neighbors)

    return neighbors


def hamming_bit_distance(x, y):
    return sum(bx != by for bx, by in zip(x, y))


def to_float_in_interval(list, nrbits, start, end):
    l = []
    for n in list:
        l.append(float(n) / (2 ** nrbits ) * (end - start) + start)
    return l


def change_bit(n, index):
    m = 1 << index
    return n ^ m

class prettyfloat(float):
    def __repr__(self):
        return "%0.2f" % self


def hillclimb(start, end, eval_function, decimals=2, axes=2, iterations=10000):
    nrbits = get_nrbits(start, end, decimals)
    best_node  = [generate_random_bits(nrbits) for x in range(0, axes)]
    best_node_float = to_float_in_interval(best_node, nrbits, start, end)
    best_eval = eval_function(best_node_float)

    print("Interval [%f %f] max bits: %d Starting Node: %s" % (start, end, nrbits, best_node_float))
    for iteration in range(0, iterations):
        current_node  = [generate_random_bits(nrbits) for x in range(0, axes)]
        current_node_float = to_float_in_interval(current_node, nrbits, start, end)
        current_eval = eval_function(current_node_float)
        neighbors = generate_all_neighbors(current_node, nrbits)
        neighbors_float = [to_float_in_interval(x, nrbits, start, end) for x in neighbors]
        #print("[%d] Current Node %s %s Eval %0.2f" %
        #    (iteration, map(prettyfloat, current_node_float), map(to_fixed_binary, current_node), current_eval))

        swapping = True
        while swapping:
            swapping = False
            neighbor = 0
            while neighbor < nrbits:
                x_float = zip(*neighbors_float)[neighbor]
                x_bits = zip(*neighbors)[neighbor] # the bit representation
                x_eval = eval_function(x_float)

                #print("\t Neighbor %s %s Eval: %0.2f Local Best: %0.2f" %
                #      (map(prettyfloat, x_float), map(to_fixed_binary, x_bits), x_eval, current_eval))

                if x_eval < current_eval:
                    current_node = x_bits
                    current_node_float = x_float
                    current_eval = x_eval
                    neighbors = generate_all_neighbors(current_node, nrbits)
                    neighbors_float = [to_float_in_interval(x, nrbits, start, end) for x in neighbors]
                    neighbor = 0
                    swapping = True

                neighbor += 1

        if best_eval > current_eval:
            best_node = current_node
            best_node_float = current_node_float
            best_eval = current_eval
            print("* New Global Best: %0.2f  %s %s"
                  % (best_eval, map(prettyfloat, best_node_float), map(to_fixed_binary, best_node)))

    print("Finished %d iterations ! Global Best: %0.2f %s" % (iterations, best_eval, map(prettyfloat, best_node_float)))
    return best_node_float

if __name__ == "__main__":
    # n = generate_all_neighbors([5], 7)
    # n = map(to_fixed_binary, *n)
    # print(to_fixed_binary(5))
    # print(n)
    start = time.time()
    h = hillclimb(-5.12, 5.12, Rastrigin().eval, 2, iterations=300)
    end = time.time()
    print("Elapsed %0.3f seconds" % (end - start ))
    print(h)