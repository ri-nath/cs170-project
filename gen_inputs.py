from starter import *
import random

def gen_graph(size, edgescale = 1):
    # random.seed(3141592)
    G = nx.empty_graph(size)
    # G.add_edge(2,1, weight=3)
    # visualize(G)
    num_edges = 0
    while num_edges < MAX_EDGES/edgescale:
        
        # print(G.nodes())
        l = []
        while len(l) == 0:
            curr = random.randrange(size)
            l = [u for u in G.nodes() if u not in G.neighbors(curr) and u != curr]
        next = l[random.randrange(len(l))]
        G.add_edge(curr, next, weight=random.randrange(1,MAX_WEIGHT))
        num_edges += 1

    return G
    
def medium(G: nx.Graph):
    G = nx.empty_graph(N_MEDIUM)
    pass
    
def large(G: nx.Graph):
    G = nx.empty_graph(N_LARGE)
    pass

# visualize(small())
G = gen_graph(N_MEDIUM)
validate_input(G)

write_input(G, "inputs/medium.in", True)