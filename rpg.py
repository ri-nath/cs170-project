from typing import Callable

import itertools
import networkx as nx
import random

from starter import *
from test import *
from shared import *
from greedy import *


#instead of picking th ebest team for each vertex it finds the best change at any state and then makes that change first before moving on 
def solver_state_based(G: nx.graph, k: int = 12, epochs: int = 5) -> nx.Graph:        
    i = 0

    for u in sorted(range(G.number_of_nodes()), key=lambda _: random.random()):
        # add_to_team(G, u, i % k)
        G.nodes[u]['team'] = i % k + 1
        i += 1

    V = G.number_of_nodes()

    for _ in range(epochs):
        sum_cost, Ck, Cw, Cp, b, bnorm = fast_update_score(None, G)
        to_add = list(range(k))
        for v in range(G.number_of_nodes()):
            if len(to_add) == 0: to_add = list(range(k))
            best_team, best_sum = G.nodes[v]['team'], float('inf')
            best_node = 0
            best_cost = []
            # best_node_overall, best_team_overall, best_sum_overall = None, G.nodes[u]['team'], float('inf')
            for u in range(G.number_of_nodes()):
                
                # _, cheapest_team = min((G.nodes[u][team], team) for team in range(k))

                # [... (heuristic, Cw, Cp, b, bnorm) ...]
                costs = [(0, 0, 0, [], 0) for team_number in range(k)]

                i = G.nodes[u]['team']
                for j in range(1, k + 1):
                    if i != j:
                        Cw_j = update_Cw(G, Cw, u, i, j)
                        b_j = list(b)
                        Cp_j, b_j, bnorm_j = update_Cp(b_j, bnorm, V, i, j)

                        delta_cost = (Cw_j - Cw) + (Cp_j - Cp)
                        costs[j - 1] = (delta_cost, Cw_j, Cp_j, b_j, bnorm_j)
                    else: 
                        costs[j - 1] = (0, Cw, Cp, b, bnorm)

                
                
                for team in range(k):
                    if costs[team][0] <= best_sum:
                        best_team = team
                        best_sum = costs[team][0]
                        best_node = u
                        best_cost = costs[team]
                
                
            G.nodes[best_node]['team'] = best_team + 1
            cost, Cw, Cp, b, bnorm = best_cost


    return G


# Adds vertex v to team team, and updates team sums to connected vertices
def solver(G: nx.graph, k: int = 12, epochs: int = 5, use_random: bool = True) -> nx.Graph:        
    i = 0
    if use_random:
        for u in sorted(range(G.number_of_nodes()), key=lambda _: random.random()):
            # add_to_team(G, u, i % k)
            G.nodes[u]['team'] = i % k + 1
            i += 1

    V = G.number_of_nodes()

    for _ in range(epochs):
        sum_cost, Ck, Cw, Cp, b, bnorm = fast_update_score(None, G)

        for u in range(G.number_of_nodes()):
            # _, cheapest_team = min((G.nodes[u][team], team) for team in range(k))

            # [... (heuristic, Cw, Cp, b, bnorm) ...]
            costs = [(0, 0, 0, [], 0) for team_number in range(k)]

            i = G.nodes[u]['team']
            for j in range(1, k + 1):
                if i != j:
                    Cw_j = update_Cw(G, Cw, u, i, j)
                    b_j = list(b)
                    Cp_j, b_j, bnorm_j = update_Cp(b_j, bnorm, V, i, j)

                    delta_cost = (Cw_j - Cw) + (Cp_j - Cp)
                    costs[j - 1] = (delta_cost, Cw_j, Cp_j, b_j, bnorm_j)
                else: 
                    costs[j - 1] = (0, Cw, Cp, b, bnorm)

            best_team, best_sum = G.nodes[u]['team'], float('inf')
            for team in range(k):
                if costs[team][0] <= best_sum:
                    best_team = team
                    best_sum = costs[team][0]
            
            G.nodes[u]['team'] = best_team + 1
            cost, Cw, Cp, b, bnorm = costs[best_team]

    return G

def test_on_all_k(G):
    best_score, B = float('inf'), None

    for k in range(1, get_k_bound(G)):
        print('Now trying k =', k)
        for _ in range(25):
            # curr_score, G_last, Ck, Cw, Cp, b, bnorm = None, None, None, None, None, None, None
            G = solver(G, k, 25)
            curr_score = score(G)
            if curr_score < best_score:
                    best_score, B = curr_score, G.copy()
                    print(k, best_score)         
    
    return B

def test_on_all_k_using_greedy(G):
    best_score, B = float('inf'), None

    for k in range(9, get_k_bound(G)):
        print('\nNow trying k =', k)
        for _ in range(25):
            # curr_score, G_last, Ck, Cw, Cp, b, bnorm = None, None, None, None, None, None, None
            G = random_for_swap(G, k, 5)
            G = solver(G, k, 15, False)
            curr_score = score(G)
            if curr_score < best_score:
                    best_score, B = curr_score, G.copy()
                    print(k, best_score)         
                    print("iteration: ", _)
    
    return B

# test_vs_output(test_on_all_k, 'inputs/large.in', 'outputs/large.out')
test_on_input(test_on_all_k, 'student_inputs/small67.in')
# test_on_input(test_on_all_k_using_greedy, 'student_inputs/small67.in')
# test_on_input(solver, 'student_inputs/small1.in')