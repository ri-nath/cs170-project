import math

import networkx as nx

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