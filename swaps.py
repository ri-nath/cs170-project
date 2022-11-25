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

import rpg

# Adds vertex v to team team, and updates team sums to connected vertices
def solver(G: nx.graph, k: int = 12, epochs: int = 5) -> nx.Graph:        
    i = 0

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
        
        # choose two vertices and mark
        # repeat until all marked
        teams = [[] for _ in range(k)]
        for v in range(V):
            teams[G.nodes[v]['team'] - 1].append(v)

        pairs = []
        while len(teams) > 1:
            t1, t2 = random.sample(range(len(teams)), 2)
            t1, t2 = min(t1, t2), max(t1, t2)
            u, v = teams[t1].pop(), teams[t2].pop()
        
            if not teams[t1]:
                del teams[t1]
                if not teams[t2 - 1]:
                    del teams[t2 - 1]
            elif not teams[t2]:
                del teams[t2]

            pairs.append((u, v))
        
        T = G.copy()
        best_so_far = total_cost
        for i in range(len(pairs)):
            u, v = pairs[i]
            tu, tv = T.nodes[u]['team'], T.nodes[v]['team']

            total_cost -= Cw
            Cw = update_Cw(T, Cw, u, tu, tv)
            T.nodes[u]['team'] = tv
            Cw = update_Cw(T, Cw, v, tv, tu)
            T.nodes[v]['team'] = tu
            total_cost += Cw

            if best_so_far > total_cost:
                best_so_far = total_cost
                G = T.copy()

        total_cost = best_so_far

        # print(total_cost, best_cost)
        if total_cost < best_cost:
            # print("LOADING COPY")
            B = G.copy()
            best_cost = total_cost
            # print("DONE LOADING")

        if last_cost == total_cost:
            count += 1
        else:
            count = 0

        # visualize(G)

    print(f'Found local minimum {best_cost} after {counter} iterations.')
    return B

def test_on_all_k(G, repeats=200):
    best_score, B = float('inf'), None

    for k in range(2, 3):
        print(f'[!!!] Now trying k={k}, with best_score={best_score}...')
        print(f'Note that the lower bound of k={k} is {calculate_Ck(k)}.')

        if calculate_Ck(k) > best_score:
                return B

        for _ in range(repeats):
            # curr_score, G_last, Ck, Cw, Cp, b, bnorm = None, None, None, None, None, None, None
            G = solver(G, k=k, epochs=5)
            curr_score = score(G)
            
            if curr_score < best_score:
                    best_score, B = curr_score, G.copy()
                    print(f'[!!] Found a new best score {best_score} with k={k}.')         
    
    return B

# test_vs_output(test_on_all_k, 'inputs/large.in', 'outputs/large.out')
# test_on_input(solver, 'student_inputs/small1.in')
# gen_outputs(test_on_all_k, 260, 'student_inputs', 'rpg_outputs')
target = lambda t: target_output(test_on_all_k, f'student_inputs/{t}.in', f'rpg_outputs_c/{t}.out')

def make_ring(n):
    n = n - 1
    G = nx.empty_graph(n)
    for i in range(n):
        G.add_edge(i, i + 1, weight=950 + i)
    G.add_edge(0, n, weight=999)

    return G

test_on_graph(test_on_all_k, make_ring(100))
# est_on_input(test_on_all_k, 'student_inputs/large1.in')
