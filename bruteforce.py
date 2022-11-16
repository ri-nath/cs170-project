import networkx as nx
import numpy as np
from starter import *
import math
import random
import itertools

def choose(S, k):
    return itertools.combinations(S, k)

# Return G\S
def without(a, b):
    return list(filter(lambda n: n not in b, a))

# Given subsets of G assign teams to subsets
def paint(G, subsets):
    for i, s in enumerate(subsets):
        for v in s:
            G.nodes[v]['team'] = i
    
def solver(G: nx.graph):
    # yield partitions of S up to size n
    def yield_partitions(S, n):
        if len(S) == n:
            yield [S]
        if len(S) > 0 and n > 0:
            # subset of size n plus partitions of S - n up to size n
            for frozen in choose(S, n):
                for rest in yield_partitions(without(S, frozen), n):
                    yield rest + [frozen]

            # partitions of S up to size n - 1
            yield from yield_partitions(S, n - 1)

    mem = {}
    best_score, B = 0, None
    for partition in yield_partitions(list(G.nodes), G.number_of_nodes()):
        paint(G, partition)
        new_score = score(G)
        print(len(partition), new_score)
        if len(partition) == 2: visualize(G)
        if not B or new_score < best_score:
            best_score, B = new_score, G.copy()

    return B

def tiny():
    size = 2
    w = 100
    G = nx.empty_graph(size * size)
    for i in range(size * size):
        if i < size*(size-1):
            G.add_edge(i, i+size, weight=w)
        if (i+1) % size != 0:
            G.add_edge(i, i+1, weight=w)
    return G

G = tiny()
visualize(G)
done = solver(G)
print(score(done))
visualize(done)
# brute = read_input('inputs/example.in')
# brute = solver(brute)

# example = read_input('inputs/example.in')
# example = read_output(example, 'outputs/example.out')

# print(score(brute), score(example))

# visualize(brute)