#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <algorithm>
#include <iostream>
#include <vector>
#include <random>

#include "graph_utils.h"
#include "rpg.h"
using namespace std;

int main(int argc, char* argv[]) {
    srand(time(0));
    graph_t *G = read_input("student_inputs/small1.in", 100);
    auto[B, score] = test_on_all_k(G, 5, true);
    printf("FINAL SCORE OF %f\n", score);
    write_output(B, "test.out");
    // double sum = 0;
    // double weights[5] = {2, 1, 1, 1, 1};
    // int32_t choices[5] = {0, 0, 0, 0, 0,};
    // for(int32_t i = 0; i < 10000; i++){
    //     double rnd = (double)rand()/(RAND_MAX/6);
    //     sum += rnd;
    //     for(int32_t i = 0; i < 5; i++){
    //         rnd -= weights[i];
    //         if(rnd <= 0){
    //             choices[i] += 1;
    //             break;
    //         }
    //     }
        // printf("%f\n", rnd);
    // }

    

    // for(int32_t i = 0; i < 5; i++){
    //     printf("average choice for %i = %i", i, choices[i]);
    // }
    // printf("HELLPPP");


    free_graph(B);

}