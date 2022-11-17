from typing import Callable

import itertools
import networkx as nx

from starter import *
from test import *
from shared import *

# given G and a subset S, returns a fn(v) which sums weights from v to S 
# def sum_weights_to_subset(G: nx.graph, S: list[int]) -> Callable[[int], int]:
#     def from_vertex(v: int) -> int:
#         edges = [G[v][u]['weight'] for u in G.neighbors(v) if u in S]
#         return sum(edges)
#     return from_vertex

# Adds vertex v to team team, and updates team sums to connected vertices
def add_to_team(G: nx.graph, teams: list[list[int]], v: int, team: int):
    G.nodes[v]['team'] = team + 1
    teams[team].append(v)
    for v, u, weight in G.edges(v, data='weight'):
        if team not in G.nodes[u]:
            G.nodes[u][team] = 0
        # Tracks sum from team to u        
        G.nodes[u][team] += weight

def solver(G: nx.graph, sources: list[int] = [40, 10, 20, 30, 0]) -> nx.Graph:    
    k = len(sources)
    teams = [[] for _ in sources]
    to_add = list(range(k))

    team = 0
    for u in G.nodes:
        if u in sources:
            add_to_team(G, teams, u, team)
            team += 1
    
    for _ in range(k, G.number_of_nodes()):
        if len(to_add) == 0: to_add = list(range(k))
        next, team = min((
            min(
                filter(lambda v: not 'team' in G.nodes[v], G.nodes), 
                key=lambda v: G.nodes[v][team] if team in G.nodes[v] else 0), 
            team)
            for team in to_add)
        to_add.remove(team)
        add_to_team(G, teams, next, team)

    return G

def test_on_all_combinations(G):
    best_score, B = float('inf'), None
    for k in range(1, get_k_bound(G)):
        for sources in itertools.combinations(G.nodes, k):
            G = solver(G, sources)
            new_score = score(G)
            if new_score < best_score:
                best_score, B = new_score, G.copy()
                print(k, best_score)
    
    return B

# test_vs_output(test_on_all_combinations)

