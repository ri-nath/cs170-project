import random
import math

import networkx as nx
import numpy as np

from starter import *
from test import *

def solver(G: nx.graph) -> nx.graph:
    mu = G.size(weight='weight') / G.size()
    k = math.floor(4 * np.log(np.sqrt(mu) * G.number_of_nodes() / 10))
    nodes = []
    for v in G.nodes:
        nodes += [v]
    random.shuffle(nodes)
    for i in range(len(nodes)):
        G.nodes[nodes[i]]['team'] = i % k
    
    return G

test_vs_output(solver)