from typing import Callable

import itertools
import networkx as nx
import random

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
def add_to_team(G: nx.graph, v: int, team: int):
    G.nodes[v]['team'] = team + 1
    for u in G.neighbors(v):
        if team not in G.nodes[u]:
            G.nodes[u][team] = 0
        # Tracks sum from team to u        
        G.nodes[u][team] += G[u][v]['weight']


def solver(G: nx.graph, k: int = 5, epochs: int = 10) -> nx.Graph:        
    i = 0

    for u in sorted(range(G.number_of_nodes()), key=lambda _: random.random()):
        # add_to_team(G, u, i % k)
        G.nodes[u]['team'] = i % k + 1
        i += 1

    for _ in range(epochs):
        for u in range(G.number_of_nodes()):
            # _, cheapest_team = min((G.nodes[u][team], team) for team in range(k))
            sums = [0] * k

            for v in G.neighbors(u):
                sums[G.nodes[v]['team'] - 1] += G[u][v]['weight']

            best_team, best_sum = G.nodes[v]['team'], float('inf')
            for team, curr_sum in enumerate(sums):
                if curr_sum < best_sum:
                    best_team = team
                    best_sum = curr_sum
                    
            G.nodes[u]['team'] = best_team + 1

    # for _ in range(k, G.number_of_nodes()):
    #     if len(to_add) == 0: to_add = list(range(k))
    #     next, team = min((
    #         min(
    #             filter(lambda v: not 'team' in G.nodes[v], G.nodes), 
    #             key=lambda v: G.nodes[v][team] if team in G.nodes[v] else 0), 
    #         team)
    #         for team in to_add)
    #     to_add.remove(team)
    #     add_to_team(G, teams, next, team)

    return G

def test_on_all_k(G):
    best_score, B = float('inf'), None

    for k in range(10, 13):
        print('Now trying k =', k)
        for _ in range(50):
            # curr_score, G_last, Ck, Cw, Cp, b, bnorm = None, None, None, None, None, None, None
            G = solver(G, k, 10)
            curr_score = score(G)
            if curr_score < best_score:
                    best_score, B = curr_score, G.copy()
                    print(k, best_score)         
    
    return B

# test_vs_output(test_on_all_k, 'inputs/large.in', 'outputs/large.out')
test_on_input(test_on_all_k, 'student_inputs/small1.in')
