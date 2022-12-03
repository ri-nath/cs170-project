#include <stdbool.h>
#include <stdio.h>
#include <tuple>
#include "graph_utils.h"

std::tuple<double, double, double, double, double, double*> first_update_score(graph_t *G);
// std::tuple<double, double, double, double, double, double*> fast_update_score(graph_t *G, graph_t *D, 
//             double ck = NULL, double cw = NULL, double cp = NULL, double bnorm = NULL, double *b, int32_t k);
std::tuple<int32_t*, double> test_on_all_k(graph_t *G, int32_t repeats = 1, bool verbose = false);
std::tuple<int32_t*, double> solver(graph_t *G, int32_t k = 12, int32_t stale = 5, double epsilon = 0.5, double decay = 1.5);