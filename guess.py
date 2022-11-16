import networkx as nx
import numpy as np
from starter import *
import random
import math

def solver(G: nx.graph):
    mu = G.size(weight='weight') / G.size()
    k = math.floor(4 * np.log(np.sqrt(mu) * G.number_of_nodes() / 10))
    nodes = []
    for v in G.nodes:
        nodes += [v]
    random.shuffle(nodes)
    for i in range(len(nodes)):
        G.nodes[nodes[i]]['team'] = i % k
    
    return G

guess = read_input('inputs/example.in')
guess = solver(guess)

example = read_input('inputs/example.in')
example = read_output(example, 'outputs/example.out')

print(score(guess), score(example))
# 512556.0841108902, 1219.2493960703473

visualize(guess)