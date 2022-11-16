from typing import Callable

import networkx as nx

from starter import *
from test import *

# given G and a subset S, returns a fn(v) which sums weights from v to S 
def sum_weights_to_subset(G: nx.graph, S: list[int]) -> Callable[[int], int]:
    def from_vertex(v: int) -> int:
        edges = [G[v][u]['weight'] for u in G.neighbors(v) if u in S]
        return sum(edges)
    return from_vertex

def solver(G: nx.graph, sources: list[int] = [0, 10, 20, 30, 40]) -> nx.Graph:    
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

test_vs_output(solver)

