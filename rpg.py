from typing import Callable

import itertools
import networkx as nx
import random
import numpy as np

from starter import *
from test import *
from shared import *
from greedy import *
from gen_files import *

# Adds vertex v to team team, and updates team sums to connected vertices
def solver(G: nx.graph, k: int = 12, epochs: int = 5, epsilon: float = 0.5, decay: float = 1.5, is_random: bool = True) -> nx.Graph:        
    i = 0
    if is_random:
        for u in sorted(range(G.number_of_nodes()), key=lambda _: random.random()):
            # add_to_team(G, u, i % k)
            G.nodes[u]['team'] = i % k + 1
            i += 1

    V = G.number_of_nodes()
    best_cost, B = float('inf'), None
    k_list = range(k)
    count, counter, last_cost = 0, 0, 0
    
    while (count < epochs) and (counter < G.number_of_nodes()):
        counter += 1
        total_cost, Ck, Cw, Cp, b, bnorm = fast_update_score(None, G)
        last_cost = total_cost
        weights = np.full(k, epsilon)
        weights = np.power(weights, k_list)
        

        for u in range(G.number_of_nodes()):
            # [... (delta_cost, Cw, Cp, b, bnorm) ...]
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

            # best_team, best_delta_cost = G.nodes[u]['team'], float('inf')
            # for team in range(k):
            #     if costs[team][0] <= best_delta_cost:
            #         best_team = team
            #         best_delta_cost = costs[team][0]
            
            # costs array
            # [... i: (delta_cost, Cw, Cp, b, bnorm) ...]
            # i = [0, k)
            # we want to sort i by delta_cost
            sorted_i = sorted(k_list, key=lambda i: costs[i][0])
            # weights = [ e ** 0, e ** 1, e ** 2 ... e ** (k - 1)]
            best_team = random.choices(sorted_i, weights=weights)[0]
            # print(sorted_i, weights, best_team)
            G.nodes[u]['team'] = best_team + 1
            delta_cost, Cw, Cp, b, bnorm = costs[best_team]
            
            total_cost += delta_cost

        epsilon = epsilon / decay
        if total_cost < best_cost:
            # print("LOADING COPY")
            B = G.copy()
            best_cost = total_cost
            # print("DONE LOADING")

        if last_cost == total_cost:
            count += 1
        else:
            count = 0
        
    print(f'Found local minimum {best_cost} after {counter} iterations.')
    return B

def test_on_all_k(G, repeats=50):
    best_score, B = float('inf'), None

    for k in range(2, calculate_k_bound(G)):
        print(f'[!!!] Now trying k={k}, with best_score={best_score}...')
        print(f'Note that the lower bound of k={k} is {calculate_Ck(k)}.')

        if calculate_Ck(k) > best_score:
                return B

        for _ in range(repeats):
            # curr_score, G_last, Ck, Cw, Cp, b, bnorm = None, None, None, None, None, None, None
            G = solver(G, k=k, epochs=5, epsilon=1, decay=1.5)
            curr_score = score(G)
            
            if curr_score < best_score:
                    best_score, B = curr_score, G.copy()
                    print(f'[!!] Found a new best score {best_score} with k={k}.')         
    
    return B

# test_vs_output(test_on_all_k, 'inputs/large.in', 'outputs/large.out')
# test_on_input(test_on_all_k, 'student_inputs/large1.in')
# test_on_input(solver, 'student_inputs/small1.in')
# gen_outputs(test_on_all_k, 260, 'student_inputs', 'rpg_outputs')
target = lambda t: target_output(test_on_all_k, f'student_inputs/{t}.in', f'rpg_outputs/{t}.out')
target('large53')
