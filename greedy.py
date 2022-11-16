import networkx as nx
import numpy as np
from starter import *
import math
import random



def solver(Gold: nx.graph):
    G = Gold.copy()
    edges = G.edges(data='weight')
    mu = G.size(weight='weight') / G.size()
    # k = math.floor(4 * np.log(np.sqrt(mu) * G.number_of_nodes() / 10))
    k = 5
    m = float('inf')
    bk = 0
    # for k in range(2,G.number_of_nodes()):
    for i in range(G.number_of_nodes()):
        G.nodes[i]['visited'] = 0
    print(k)
    prev = [None for _ in range(k)]
    teams = [[] for _ in range(k)]
    u, v, _ = sorted(edges, reverse=True, key=lambda x: x[2])[0]
    # team = 0
    # G.nodes[u]['team'] = team
    # G.nodes[u]['visited'] = 1
    # prev[team] = u
    # teams[team] += [u]
    
    # team += 1
    # for i in range(1, k):
    #     pre = (team-1)%k
    #     print("pre: ", pre)
    #     print("prev: ", prev)
    #     next = max([u for u in G.neighbors(prev[pre]) if G.nodes[u]['visited'] == 0], key=lambda x: G[prev[pre]][x]['weight'])
    #     print("weight: ", G[prev[pre]][next]['weight'])
    #     G.nodes[next]['visited'] = 1
    #     G.nodes[next]['team'] = team % k
    #     prev[team%k] = next
    #     teams[team%k] += [next]
    #     team += 1
    team = 0
    prev = [0, 10, 20, 30, 40]
    teams = [[0], [10], [20], [30], [40]]
    for u in prev:
        G.nodes[u]['team'] = team
        G.nodes[u]['visited'] = 1
        team += 1
    print("--------------------------------------------")
    while team < G.number_of_nodes():
        curr = (team)%k
        print("curr: ", curr)
        print("prev: ", prev)
        print("teams: ", teams)
        next = min([n for n in G.nodes() if G.nodes[n]['visited'] == 0], key=lambda x: sum([G[u][x]['weight'] for u in G.neighbors(x) if u in [u for u in teams[curr]]]))
        G.nodes[next]['visited'] = 1
        G.nodes[next]['team'] = team % k
        prev[team%k] = next
        teams[team%k] += [next]
        team += 1

    
    
    
    # for u, v, _ in sorted(edges, reverse=False, key=lambda x: x[2]):
    #     if 'team' in G.nodes[u] and 'team' in G.nodes[v]:
    #         pass
    #     elif 'team' in G.nodes[u]:
    #         G.nodes[v]['team'] = team
    #         team = team + 1 % k
    #     elif 'team' in G.nodes[v]:
    #         G.nodes[u]['team'] = team
    #         team = team + 1 % k
    #     else:
    #         G.nodes[u]['team'] = team
    #         G.nodes[v]['team'] = team + 1 % k
    #         team = team + 2 % k
    s = score(G)
    if(s < m):
        m = s
        bk = k
        Gout = G.copy()
    print("MIN__________________: ", m)

    # Band-aid patch, teams should be one-indexed
    for v in Gout.nodes:
        Gout.nodes[v]['team'] = Gout.nodes[v]['team'] + 1
    return Gout

greedy = read_input('inputs/example.in')
greedy = solver(greedy)

example = read_input('inputs/example.in')
example = read_output(example, 'outputs/example.out')

print(score(greedy, separated=True), score(example, separated=True))

# visualize(greedy)
