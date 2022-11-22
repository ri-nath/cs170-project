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
def sum_weights_to_subset(G: nx.graph, S: list[int]) -> Callable[[int], int]:
    def from_vertex(v: int) -> int:
        edges = [G[v][u]['weight'] for u in G.neighbors(v) if u in S]
        return sum(edges)
    return from_vertex

def greedy(G: nx.graph, sources: list[int] = [0, 10, 20, 30, 40]) -> nx.Graph:    
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

def add_to_team(G: nx.graph, teams: list[list[int]], v: int, team: int):
    G.nodes[v]['team'] = team + 1
    teams[team].append(v)
    for u in G.neighbors(v):
        if team not in G.nodes[u]:
            G.nodes[u][team] = 0
        # Tracks sum from team to u        
        G.nodes[u][team] += G[u][v]['weight']

def solver_all_teams(G: nx.graph, sources: list[int] = [40, 10, 20, 30, 0]) -> nx.Graph:    
    k = len(sources)
    teams = [[] for _ in sources]
    to_add = list(range(k))

    team = 0
    for u in sources:
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

def test_random(G, epochs: int = 10):
    best_score, B = float('inf'), None

    for _ in range(epochs):

        for k in range(1, get_k_bound(G)):
            lst = sorted(range(G.number_of_nodes()), key=lambda _: random.random())
            # add_to_team(G, u, i % k)
            sources = [None for _ in range(k)]
            for i in range(k):
                sources[i] = lst[i]
            res = greedy(G, sources)
            if(score(res) < best_score):
                best_score = score(res)
                B = res.copy()
    return B
            

            
# def random_for_swap(G, k, epochs: int = 1):
#     lst = sorted(range(G.number_of_nodes()), key=lambda _: random.random())
#     # add_to_team(G, u, i % k)
#     sources = [None for _ in range(k)]
#     for i in range(k):
#         sources[i] = lst[i]
#     res = greedy(G, sources)
#     return res.copy()

def random_for_swap(G, k, epochs: int = 1):   
    best_score, B = float('inf'), None

    for _ in range(epochs):

        lst = sorted(range(G.number_of_nodes()), key=lambda _: random.random())
        # add_to_team(G, u, i % k)
        sources = [None for _ in range(k)]
        for i in range(k):
            sources[i] = lst[i]
        res = greedy(G, sources)
        if(score(res) < best_score):
            best_score = score(res)
            B = res.copy()
    return B



def test_on_all_combinations(G):
    best_score, B = float('inf'), None

    for k in range(1, get_k_bound(G)):
        print('Now trying k =', k)
        curr_score, G_last, Ck, Cw, Cp, b, bnorm = None, None, None, None, None, None, None
        
        for sources in itertools.combinations(G.nodes, k):
            # print(sources)
            D = greedy(G.copy(), sources)
            curr_score, Ck, Cw, Cp, b, bnorm = fast_update_score(G_last, D, Ck, Cw, Cp, b, bnorm)
            
            # assert abs(curr_score - score(D)) < 0.000001

            G_last = D
            if curr_score < best_score:
                best_score, B = curr_score, D.copy()
                print(k, best_score)
    
    return B

# test_on_input( test_random,'student_inputs/small40.in')

