#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#include "graph_utils.h"
using namespace std;

int main(int argc, char* argv[]) {
    graph_t *G = read_input("inputs/example.in", 100);
    printf("HELLPPP");
    free_graph(G);
}