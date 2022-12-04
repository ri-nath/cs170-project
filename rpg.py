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

# ALGORITHM:
# Evenly partition graph into k groups. 
# Then, for every vertex v, move v to a better team with high probability, or a random team with low probability.
# Decrease 'temperature' over time: As the algorithm iterates, the probability of choosing a random team decreases exponentially.
# Stop iterating once the algorithm cannot escape a local minimum.
def solver(G: nx.graph, k: int = 12, epochs: int = 5, epsilon: float = 0.5, decay: float = 1.5) -> nx.Graph:        
    # Randomly partition G into k - 1 evenly sized teams, and one team of size V % k.
    i = 0
    for u in sorted(range(G.number_of_nodes()), key=lambda _: random.random()):
        G.nodes[u]['team'] = i % k + 1
        i += 1

    V = G.number_of_nodes()
    best_cost, B = float('inf'), None
    count, counter, last_cost = 0, 0, 0

    # Initialize fast scoring partials.
    total_cost, Ck, Cw, Cp, b, bnorm = fast_update_score(None, G)
    last_cost = total_cost
    
    while count < epochs and (counter < G.number_of_nodes()):
        counter += 1

        weights = np.full(k, epsilon)
        weights = np.power(weights, range(k))

        last_cost = total_cost
        
        # For every vertex u, move u to a better team with high probability, 
        # or a random team with low probability.
        for u in range(G.number_of_nodes()):
            # We structure the costs array to remember partials necessary for fast scoring.
            # costs[i] = (delta_cost_i, Cw_i, Cp_i, b_i, bnorm_i)
            costs = [(0, 0, 0, [], 0) for team in range(k)]

            # Consider swapping vertex u from its own team i to all teams j. 
            i = G.nodes[u]['team']
            for j in range(1, k + 1):
                if i != j:
                    Cw_j = update_Cw(G, Cw, u, i, j)
                    b_j = list(b)
                    Cp_j, b_j, bnorm_j = update_Cp(b_j, bnorm, V, i, j)

                    delta_cost = (Cw_j - Cw) + (Cp_j - Cp)
                    costs[j - 1] = (delta_cost, Cw_j, Cp_j, bnorm_j)
                else: 
                    costs[j - 1] = (0, Cw, Cp, bnorm)

            # Sort the teams by minimizing for the cost of swapping vertex u to that team.
            # Then, pick a team with probabilities weighted towards better choices. 
            sorted_i = sorted(range(k), key=lambda i: costs[i][0])
            best_team = random.choices(sorted_i, weights=weights)[0]

            # Update the graph and fast scoring partials.
            delta_cost, Cw, Cp, bnorm = costs[best_team]
            b[G.nodes[u]['team']-1] -= 1/G.number_of_nodes()
            b[best_team] += 1/G.number_of_nodes()
            G.nodes[u]['team'] = best_team + 1
            

            total_cost += delta_cost

        # Decrease the 'temperature' of the function. Epsilon approaches zero with many iterations.
        epsilon = epsilon / decay

        # Always save the best iteration in case we don't come back to it.
        if total_cost < best_cost:
            B = G.copy()
            best_cost = total_cost

        # If we are stuck in a local minimum, stop iterating.
        if last_cost == total_cost:
            count += 1
        else:
            count = 0
        
    return B, best_cost

# ALGORITHM
# Run solver on all k from k=1 to k=max viable k.
# Repeat the solver repeats times on each k.
# Because solver randomly distributes groups, this has the effect of
# uniformly distributing starting points in R{V}. This maximizes the probability
# of landing near the global minimum at least once.
def test_on_all_k(G, repeats=1, verbose=True):
    best_score, B = float('inf'), None

    for k in range(1, calculate_k_bound(G)):
        LOWER_BOUND = calculate_Ck(k) + 1.0

        if verbose:
            print(f'[!!!] Now trying k={k}, with best_score={best_score}...')
            print(f'Note that the lower bound of k={k} is {LOWER_BOUND}.')

        # If our best score is better than the lower bound, 
        # which is given by LOWER_BOUND = 0 + Ck(k) + 1.0,
        # stop iterating. 
        if LOWER_BOUND > best_score:
            return B

        for _ in range(repeats):
            G, cost = solver(G, k=k, epochs=5, epsilon=1, decay=1.5)
            curr_score = score(G)
            print(f'curr_score = {cost}, should be {curr_score}')
            
            if curr_score < best_score:
                best_score, B = curr_score, G.copy()
                if verbose:
                    print(f'[!!] Found a new best score {best_score} with k={k}.')         
    
    return B

tar("rpg_outputs_a")
# gen_outputs(test_on_all_k, 'student_inputs', 'rpg_outputs')
