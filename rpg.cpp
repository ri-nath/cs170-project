#include "rpg.h"

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <random>
#include <algorithm>
#include <vector>
#include <cmath>
#include <tuple>
#include <list>

#include "graph_utils.h"

#define K_COEFFICIENT 100
#define B_EXP 70
#define K_EXP 0.5

/*
G is a graph
K is the number of teams
stale is the number of times the graph has to be unchanged to terminate
epsilon is the weight multiplier
decay is what scales epsilon each timestep.
*/
graph_t* solver(graph_t *G, int32_t k = 12, int32_t stale = 5, double epsilon = 0.5, double decay = 1.5){
    //assigns random teams to the vertices
    std::list<int32_t> scramble;
    for (int32_t i = 0; i < G->num_nodes; i++){
        scramble.push_back(i);
    }
    std::random_shuffle(scramble.begin(), scramble.end());

    for (int32_t i = 0; i < G->num_nodes; i++){
        int32_t curr = scramble.back();
        scramble.pop_back();
        G->nodes[curr].team = i%k;
    }

    double best_cost = INFINITY;
    double *b = NULL;
    int32_t k_list[k];
    for(int32_t i = 0; i < k; i++) k_list[i] = i;
    int32_t count = 0;
    int32_t counter = 0;
    double last_cost = 0;

    while((count < stale) && (counter < G->num_nodes)){
        counter++;
        
    }
}


int32_t calculate_k_bound(graph_t *G){
    return (int32_t) 2 * log((G->num_edges/100) + sqrt(exp(1)));
}

double calculate_ck(int32_t k){
    return K_COEFFICIENT * exp(K_EXP * k);
}

/*
v is the number of nodes
i is original team 0 indexed
j is new team 0 indexed

returns cp, b, bnorm
*/
std::tuple<double, double, double*> update_cp(double *b, double bnorm, int32_t v, int32_t i, int32_t j){
    bnorm = sqrt(pow(bnorm, 2) - pow(b[i], 2) - pow(b[j], 2)
        + pow(b[i] - 1/v, 2) + pow(b[j] + 1/v, 2)); 
    b[i] -= 1/v;
    b[j] += 1/v;

    double cp = exp(B_EXP*bnorm);

    return {cp, bnorm, b};
}

int32_t update_cw(graph_t *G, int32_t cw, int32_t u, int32_t i, int32_t j){
    for(int32_t i = 0; i < G->nodes[u].num_neighbors; i++){
        int32_t v = G->nodes[u].neighbors[i].target;
        if(G->nodes[v].team == i){
            cw -= G->nodes[u].neighbors[i].weight;
        }else if(G->nodes[v].team == j){
            cw += G->nodes[u].neighbors[i].weight;
        }
    }

    return cw;
}

/*
G is new Graph
D is new Graph
*/
std::tuple<double, double, double, double, double, double*> fast_update_score(graph_t *G, graph_t *D, 
            double ck = NULL, double cw = NULL, double cp = NULL, double bnorm = NULL, double *b){
    if(!ck) {
        return first_update_score(D);
    }
    
    std::list<int32_t> different_vertices;

    for(int i = 0; i < G->num_nodes; i++){
        if(G->nodes[i].team != D->nodes[i].team){
            different_vertices.push_back(i);
        }
    }

    //your code here
    for (std::list<int32_t>::iterator it = different_vertices.begin(); it != different_vertices.end(); ++it){
        int32_t new_team = D->nodes[*it].team;
        int32_t old_team = G->nodes[*it].team;
        auto[cp_new, bnorm_new, b_new] = update_cp(b, bnorm, G->num_nodes, old_team, new_team);
        double cw_new = update_cw(G, cw, *it, old_team, new_team);
        cw = cw_new;
        cp = cp_new;
        bnorm = bnorm_new;
        b = b_new;
        G->nodes[*it].team = new_team;
    }

    return {(cw+ ck + cp), ck, cw, cp, bnorm, b};

}

//return is cost, ck, cw, cp, bnorm, b
std::tuple<double, double, double, double, double, double*> first_update_score(graph_t *G){
    int32_t k = 0;
    int32_t counts[20] = {0};
    int32_t max;
    for(int32_t i = 0; i < G->num_nodes; i++){
        if(counts[G->nodes[i].team] == 0){
            k++;
        }
        counts[G->nodes[i].team]++;
        if(counts[G->nodes[i].team] > max){
            max = counts[G->nodes[i].team];
        }
    }
    double *b = (double *) calloc(k, sizeof(int32_t));
    for(int32_t i = 0; i < k; i++){
        b[i] = (counts[i] /G->num_nodes) - (1/k);
    }
    
    double bnorm = norm(b, k);

    double cw = 0;

    for(int32_t i = 0; i < G->num_nodes; i++){
        for(int32_t j = 0; j < G->nodes[i].num_neighbors; j++){
            int32_t source = G->nodes[i].neighbors[j].source;
            int32_t target = G->nodes[i].neighbors[j].target;
            int32_t weight = G->nodes[i].neighbors[j].weight;
            if(G->nodes[source].team == G->nodes[target].team){
                //divided by two to account for double counting
                cw += weight/2; 
            }
        }
    }

    double ck = K_COEFFICIENT * exp(K_EXP * k);
    double cp = exp(B_EXP * bnorm);

    return {(cw + ck + cp), ck, cw, cp, bnorm, b};
}

double norm(double *array, size_t length){
    double sum = 0;
    for(int i = 0; i < length; i++){
        sum += pow(array[i], 2);
    }
    return sqrt(sum);
}