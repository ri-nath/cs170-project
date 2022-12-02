#ifndef _GRAPH_UTILS_H
#define _GRAPH_UTILS_H

#include <stdbool.h>
#include <stdio.h>
#include <stdint.h>

typedef struct edge_t {
    int32_t source;
    int32_t target;
    int32_t weight;
} edge_t;

typedef struct node_t {
    int32_t team;
    edge_t *neighbors;
    int32_t max_neighbors;
    int32_t num_neighbors;
    
} node_t;

typedef struct graph_t {
    int32_t num_nodes;
    int32_t num_edges;
    int64_t sum_weights;
    node_t *nodes;
} graph_t;

graph_t* read_input(const char *path, int32_t size);
graph_t* copy(graph_t* G);
void free_graph(graph_t* G);
void write_output(graph_t *G, const char *path);
void gen_outputs(graph_t* (*solver)(graph_t*, int32_t, bool), const char *in, const char *out);
#endif