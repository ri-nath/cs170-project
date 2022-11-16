import itertools
from typing import Iterator

import networkx as nx

from starter import *
from test import *

# Return G\S
def without(a: list[int], b: list[int]) -> list[int]:
    return list(filter(lambda n: n not in b, a))

# Given subsets of G assign teams to subsets
def paint(G: nx.graph, subsets: list[list[int]]) -> None:
    for i, s in enumerate(subsets):
        for v in s:
            G.nodes[v]['team'] = i + 1 # 1-indexed?

# yield partitions of S up to size n
def yield_partitions(S: list[int], n: int) -> Iterator[list[int]]:
    if len(S) == n:
        yield [S]
    if len(S) > 0 and n > 0:
        # subset of size n plus partitions of S - n up to size n
        for frozen in itertools.combinations(S, n):
            for rest in yield_partitions(without(S, frozen), n):
                yield rest + [frozen]

        # partitions of S up to size n - 1
        yield from yield_partitions(S, n - 1)

def solver(G: nx.graph) -> nx.graph:
    best_score, B = 0, None
    for partition in yield_partitions(list(G.nodes), G.number_of_nodes()):
        paint(G, partition)
        new_score = score(G)
        if not B or new_score < best_score:
            best_score, B = new_score, G.copy()
            print(best_score) # Uncomment for logging

    return B

# Test on small graph
test_on_simple_graph(solver)

# Test on large graph (takes a lot of time)
# test_vs_output(solver)