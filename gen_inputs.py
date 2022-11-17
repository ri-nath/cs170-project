from starter import *
from greedy import solver
import random

MIN_TOTAL_WEIGHT = 500000

def gen_graph(n):
    G = nx.empty_graph(n)
    k = random.choices(list(filter(lambda x: n % x == 0, range(4, 12))))[0]
    k = 5
    teams = [[] for _ in range(k)]
    for i, v in enumerate(random.sample(list(range(n)), n)):
    #for i, v in enumerate(list(range(n))):
        teams[i % k].append(v)
    
    num_edges = random.randint(n, MAX_EDGES / 2)
    min_weight = 1 + MIN_TOTAL_WEIGHT // num_edges

    while num_edges > 0:
        allies = random.randint(0, k - 1)
        enemies = random.randint(0, k - 1)
        while enemies == allies:
            enemies = random.randint(0, k - 1)

        friend = random.choices(teams[allies])[0]
        foe = random.choices(teams[enemies])[0]
        if not G.has_edge(friend, foe):
            G.add_edge(friend, foe, weight = random.randint(min_weight, MAX_WEIGHT))
            num_edges -= 1

    for u in G.nodes:
        for v in G.nodes:
            if v != u and not G.has_edge(u, v):
                G.add_edge(u, v, weight = 0)

    print([team[0] for team in teams])
    solved_greedily = solver(G.copy(), sorted([team[0] for team in teams]))
    print(score(solved_greedily))
    visualize(solved_greedily)
    
    for i in range(k):
        for v in teams[i]:
            G.nodes[v]['team'] = i
    
    print(score(G))
    visualize(G)
    return G

gen_graph(N_SMALL)