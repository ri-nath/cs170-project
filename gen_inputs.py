from starter import *
from greedy import solver
import random

MIN_TOTAL_WEIGHT = 500000

def gen_graph(n, debug=False, k=None):
    G = nx.empty_graph(n)
    if not k: k = random.choices(list(filter(lambda x: n % x == 0, range(4, 12))))[0]

    teams = [[] for _ in range(k)]
    for i, v in enumerate(random.sample(list(range(n)), n)):
        teams[i % k].append(v)
    
    num_edges = MAX_EDGES
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
    
    O = G.copy()
    for i in range(k):
        for v in teams[i]:
            O.nodes[v]['team'] = i + 1
    
    visualize(O)

    if (debug):
        solved_greedily = solver(G.copy(), [team[0] for team in teams])
        print("Greedy:", score(solved_greedily))
        print("Optimal:", score(O))

        if score(O) != score(solved_greedily):
            visualize(solved_greedily)

    return G, O

def gen_graphs_for_phase_1():
    small_in, small_out = gen_graph(N_SMALL, k=10)
    medium_in, medium_out = gen_graph(N_MEDIUM, k=12)
    large_in, large_out = gen_graph(N_LARGE, k=10)

    write_input(small_in, 'inputs/small.in', overwrite=True)
    write_input(medium_in, 'inputs/medium.in', overwrite=True)
    write_input(large_in, 'inputs/large.in', overwrite=True)

    write_output(small_out, 'outputs/small.out', overwrite=True)
    write_output(medium_out, 'outputs/medium.out', overwrite=True)
    write_output(large_out, 'outputs/large.out', overwrite=True)

def check_graphs():
    def check_graph(i, o):
        G = read_input(i)
        validate_input(G)
        visualize(G)

        O = read_output(G, o)
        validate_output(O)
        visualize(O)

    check_graph('inputs/small.in', 'outputs/small.out')
    check_graph('inputs/medium.in', 'outputs/medium.out')
    check_graph('inputs/large.in', 'outputs/large.out')

check_graphs()