import networkx as nx
import numpy as np
from starter import *
import math
import random

# given G and a subset S, returns a fn(v) which sums weights from v to S 
def sum_weights_to_subset(G, S):
    def from_vertex(v):
        edges = [G[v][u]['weight'] for u in G.neighbors(v) if u in S]
        return sum(edges)
    return from_vertex

def solver(G: nx.graph, sources: list[int] = [0, 10, 20, 30, 40]):    
    k = len(sources)
    teams = [[s] for s in sources]

    team = 0
    for u in G.nodes:
        if u in sources:
            G.nodes[u]['team'] = team + 1
            G.nodes[u]['visited'] = True
            team += 1
        else:
            G.nodes[u]['visited'] = False
    
    for i in range(k, G.number_of_nodes()):
        team = i % k
        not_visited = filter(lambda v: not G.nodes[v]['visited'], G.nodes)
        next = min(not_visited, key=sum_weights_to_subset(G, teams[team]))
        G.nodes[next]['team'] = team + 1
        G.nodes[next]['visited'] = True
        teams[team].append(next)

    return G

greedy = read_input('inputs/example.in')
greedy = solver(greedy)

example = read_input('inputs/example.in')
example = read_output(example, 'outputs/example.out')

print(score(greedy), score(example))

visualize(greedy)
