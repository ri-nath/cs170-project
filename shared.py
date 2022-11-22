import math

import networkx as nx
import numpy as np

SQRT_E = math.sqrt(math.e)

def get_k_bound(G: nx.graph) -> int:
    # 1. Define C(n) = 0 + 100 * e^(n/2) + 1 to be the best possible cost for k = n.
    # 2. C(1) is a constant, C(1) = W + 100 * sqrt(e) + 1 
    # 3. If C(n) >= C(1), it is useless to check sols with k >= n as we can just use k = 1.
    # 4. We want C(n) < C(1), what is the highest possible n that satisfies this?
    # 5. 0 + 100 * e^(n/2) + 1 < W + 100 * sqrt(e) + 1 
    # e ^ n < (W / 100 + sqrt(e))^2
    # n < 2 * ln (W / 100 + sqrt(e))
    # 6. k = floor[[n]] as we only consider integer k and we have found a tight bound.
    W = G.size(weight='weight')
    return math.floor(2 * math.log(W / 100 + SQRT_E))

K_COEFFICIENT = 100
B_EXP = 70
K_EXP = 0.5

def update_Cp(b: np.array, bnorm: float, V: int, i: int, j: int) -> tuple[float, float, np.array]:
    # Account for zero-indexing of b
    i = i - 1
    j = j - 1

    try:
        bnorm = math.sqrt(
            bnorm ** 2 - b[i] ** 2 - b[j] ** 2 
            + (b[i] - 1 / V) ** 2 + (b[j] + 1 / V) ** 2
            )
        b[i] -= 1 / V
        b[j] += 1 / V
    # Account for floating point error when b norm is zero
    except ValueError:
        bnorm = 0
        b = np.zeros(len(b))

    # assert abs(bnorm - np.linalg.norm(b)) < 0.0001

    Cp = math.exp(B_EXP * bnorm)

    return Cp, b, bnorm

def update_Cw(G: nx.graph, Cw: int, v: int, i: int, j: int):
    for u in G.neighbors(v):
        if G.nodes[u]['team'] == i:
            Cw -= G[v][u]['weight']
        elif G.nodes[u]['team'] == j:
            Cw += G[v][u]['weight']

    return Cw

def fast_update_score(G: nx.graph, D: nx.graph, 
                      Ck: float = None, Cw: float = None, Cp: float = None, 
                      b: np.array = None, bnorm: float = None) -> tuple[float, float, float, float, np.array, float]:
    if not Ck:
        return first_update_score(D)


    V = G.number_of_nodes()

    different_vertices = [(v, new_team) for v, new_team in D.nodes(data='team') if new_team != G.nodes[v]['team']]
    for v, new_team in different_vertices:
        old_team = G.nodes[v]['team']
        Cp, b, bnorm = update_Cp(b, bnorm, V, old_team, new_team)

        Cw = update_Cw(G, Cw, v, old_team, new_team)
        G.nodes[v]['team'] = new_team

    return sum((Ck, Cw, Cp)), Ck, Cw, Cp, b, bnorm

def first_update_score(G: nx.graph) -> tuple[float, float, float, float, np.array, float]:
    output = [G.nodes[v]['team'] for v in range(G.number_of_nodes())]
    teams, counts = np.unique(output, return_counts=True)

    k = np.max(teams)
    b = counts / G.number_of_nodes() - 1 / k
    bnorm = np.linalg.norm(b, 2)
    Cw = sum(d for u, v, d in G.edges(data='weight') if output[u] == output[v])
            
    Ck = K_COEFFICIENT * math.exp(K_EXP * k)
    Cp = math.exp(B_EXP * bnorm)

    return sum((Ck, Cw, Cp)), Ck, Cw, Cp, b, bnorm
