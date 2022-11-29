#include "graph_utils.h"

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <iostream>
#include <nlohmann/json.hpp>
using json = nlohmann::json;

//declare helpers
void add_edge(graph_t* G, int32_t source, int32_t target, int32_t weight);
void resize(graph_t *G, int32_t index);

//size is number of nodes
graph_t* read_input(const char *path, int32_t size){
    FILE *file;
    file = fopen(path, "r");
    if(file == NULL) return NULL;
    graph_t *G = (graph_t*) calloc(1, sizeof(graph_t));
    G->nodes = (node_t*) calloc(size, sizeof(node_t));
    G->num_nodes = size;
    for(int32_t i = 0; i < size; i++){
        G->nodes[i].neighbors = (edge_t*) calloc(8, sizeof(edge_t));
        G->nodes[i].max_neighbors = 8;
    }

    json data = json::parse(file);
    json dat = data["links"];
    for (int32_t i = 0; i < dat.size(); i++) {
        json curr = dat.at(i);
        // printf("FROM: %d, TO: %d, WEIGHT: %d\n", (int32_t)curr["source"], (int32_t)curr["target"], (int32_t)curr["weight"]);
        add_edge(G, (int32_t)curr["source"], (int32_t)curr["target"], (int32_t)curr["weight"]);
        G->num_edges++;
    }

    fclose(file);

    return G;
}

void gen_outputs(graph_t* (*solver)(graph_t*, int32_t, bool), const char *in, const char *out){

}

void write_output(graph_t *G, const char *path){
    FILE *f;
    fprintf(f, "[");
    for(int i = 0; i < G->num_nodes - 1; i++){
        fprintf(f, "%d, ", G->nodes[i].team+1);
    }
    fprintf(f, "%d]", G->nodes[G->num_nodes - 1].team+1);
    fclose(f);
}

void resize(graph_t *G, int32_t index){
    if(G->nodes[index].num_neighbors + 1 == G->nodes[index].max_neighbors){
        G->nodes[index].max_neighbors *= 2;
        edge_t *new_edges = (edge_t*) calloc(G->nodes[index].max_neighbors, sizeof(edge_t));
        for(int32_t i = 0; i < G->nodes[index].max_neighbors/2; i++){
            new_edges[i].source = G->nodes[index].neighbors[i].source;
            new_edges[i].target = G->nodes[index].neighbors[i].target;
            new_edges[i].weight = G->nodes[index].neighbors[i].weight;
        }
        free(G->nodes[index].neighbors);
        G->nodes[index].neighbors = new_edges;
    }
}

void add_edge(graph_t *G, int32_t source, int32_t target, int32_t weight){
    //adjust memory allocations
    resize(G, source);
    resize(G, target);
    //set source to target
    G->nodes[source].neighbors[G->nodes[source].num_neighbors].source = source;
    G->nodes[source].neighbors[G->nodes[source].num_neighbors].target = target;
    G->nodes[source].neighbors[G->nodes[source].num_neighbors].weight = weight;
    G->nodes[source].num_neighbors += 1;
    //set target to source
    G->nodes[target].neighbors[G->nodes[target].num_neighbors].source = target;
    G->nodes[target].neighbors[G->nodes[target].num_neighbors].target = source;
    G->nodes[target].neighbors[G->nodes[target].num_neighbors].weight = weight;
    G->nodes[target].num_neighbors += 1;
}

void free_graph(graph_t* G){
    for(int32_t i = 0; i < G->num_nodes; i++){
        printf("freeing node %i's neighbors\n", i);
        free(G->nodes[i].neighbors);
    }
    printf("freeing nodes\n");
    free(G->nodes);
    printf("freeing graph\n");
    free(G);
    printf("successfully freed graph\n");
}

graph_t* copy(graph_t* G){
    graph_t *B = (graph_t*) calloc(1, sizeof(graph_t));
    B->nodes = (node_t*) calloc(G->num_nodes, sizeof(node_t));
    B->num_nodes = G->num_nodes;
    B->num_edges = G->num_edges;
    for(int32_t i = 0; i < G->num_nodes; i++){
        B->nodes[i].neighbors = (edge_t*) calloc(G->nodes[i].max_neighbors, sizeof(edge_t));
        B->nodes[i].max_neighbors = G->nodes[i].max_neighbors;
        B->nodes[i].team = G->nodes[i].team;
    }
    for(int32_t i = 0; i < G->num_nodes; i++){
        for(int32_t j = 0; j < G->nodes[i].num_neighbors; j++){
            if(G->nodes[i].neighbors[j].target > i){
                add_edge(B, G->nodes[i].neighbors[j].source, G->nodes[i].neighbors[j].target, G->nodes[i].neighbors[j].weight);
            }
        }
    }
    return B;
}