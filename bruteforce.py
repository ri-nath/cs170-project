import networkx as nx
import numpy as np
from starter import *
import math
import random
import itertools

# Return G\S
def without(a: list[int], b: list[int]):
    return list(filter(lambda n: n not in b, a))

# Given subsets of G assign teams to subsets
def paint(G: nx.graph, subsets: list[list[int]]):
    for i, s in enumerate(subsets):
        for v in s:
            G.nodes[v]['team'] = i + 1 # 1-indexed?

# yield partitions of S up to size n
def yield_partitions(S: list[int], n: int):
    if len(S) == n:
        yield [S]
    if len(S) > 0 and n > 0:
        # subset of size n plus partitions of S - n up to size n
        for frozen in itertools.combinations(S, n):
            for rest in yield_partitions(without(S, frozen), n):
                yield rest + [frozen]

        # partitions of S up to size n - 1
        yield from yield_partitions(S, n - 1)

def solver(G: nx.graph):
    best_score, B = 0, None
    for partition in yield_partitions(list(G.nodes), G.number_of_nodes()):
        paint(G, partition)
        new_score = score(G)
        if not B or new_score < best_score:
            best_score, B = new_score, G.copy()
            # print(best_score) # Uncomment if want logging

    return B

### TESTS ###
def test_on_tiny():
    def tiny(W, H):
        weight = 100
        G = nx.empty_graph(W * H)
        for i in range(W * H):
            if i < W*(H-1):
                G.add_edge(i, i+W, weight=weight)
            if (i+1) % W != 0:
                G.add_edge(i, i+1, weight=weight)
        return G

    alg = tiny(2, 3)
    alg = solver(alg)
    print("Score of brute-force on tiny:", score(alg))
    visualize(alg)

def test_on_example():
    alg = read_input('inputs/example.in')
    alg = solver(alg)

    example = read_input('inputs/example.in')
    example = read_output(example, 'outputs/example.out')

    print("Score of brute-force on example:", score(alg))
    print("Score of example on example:", score(example));
    visualize(alg)

test_on_tiny()
# test_on_example()