#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <algorithm>
#include <iostream>
#include <vector>
#include <random>
#include <string>

#include "graph_utils.h"
#include "rpg.h"
using namespace std;

int main(int argc, char* argv[]) {
    srand(time(0));
    std::string input_dir = "student_inputs/";
    std::string input_ext = ".in";
    std::string output_dir = "rpg_outputs/";
    std::string output_ext = ".out";
    std::string sizes[3] = {"small", "medium", "large"};
    int32_t lengths[3] = {100, 300, 1000};
    for(int32_t size = 0; size < 3; size++){
        for(int32_t num = 1; num < 261; num++){
            std::string curr = sizes[size];
            curr = curr + std::to_string(num);
            graph_t *G = read_input((input_dir + curr + input_ext).c_str(), lengths[size]);
            auto[B, score] = test_on_all_k(G, 5);
            printf("FINAL SCORE OF %f\n", score);
            write_output(B, lengths[size], (output_dir + curr + output_ext).c_str());
            free_graph(G);
            free(B);
        }
    }
    // graph_t *G = read_input("student_inputs/medium1.in", 300);
    // auto[B, score] = test_on_all_k(G, 5);
    // printf("FINAL SCORE OF %f\n", score);
    // write_output(B, 300, "test.out");
    // free_graph(G);
    // free(B);

}