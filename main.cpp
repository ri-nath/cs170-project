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
// #include <omp.h>

#include "graph_utils.h"
#include "rpg.h"
using namespace std;


std::string to_improve[] = {"medium94", "medium47", "large94", "medium69", "large47", "medium249", "large122", "large160", "large218", 
"small58", "small226", "large69", "large84", "large120", "large229", "large258", "large53", "large83", "large216", "large42", "large206", "small176", "medium41", "large3", "small47", "large129", "large184", "small94", "small154", "small158", "large249", "medium99", "large230", "small99", "small160", "medium83", "large105", "medium115", "small192", "medium227", "small84", "large202", "small123", "medium229", "large209", "medium127", "large62", "small12", "small13", "medium146", "large70", "large99", "small146", "small229", "medium176", "large197", "large146", "small215", "large162", "small83", "large11", "large215", "medium13", "medium160", 
"small108", "medium50", "large157", "medium14", "medium70", "medium156", "large200", "large14", "small125", 
"medium215", "medium230", "medium98", "large241", "medium197", "large117", "large235", "medium236", "medium232", "large49", "large102", "large169", "large182", "small245", "small259", "large2", "large95", "large111", "large144", "large155", "large257", "small156", "medium123", "medium192", "medium239", "large29", "large58", "large87", "large145", "medium97", "large31", "large33", "large80", "large214", "large248", "small70", "small114", "small115", "medium87", "large32", "large73", "large138", "large150", "large180", "large201", "large234", "small184", "medium21", "medium210", "medium259", "large17", "large23", "large25", "large38", "large140", "large177", "large198", "large219", "small177", "small238", "small249", "medium63", "medium129", "medium152", "medium225", "medium244", "large7", "large9", "large64", "large67", "large109", "large124", "large137", "large186", "small236", "medium25", "medium42", "medium254", "large34", "large54", "large98", "large123", "large192", "large227", "large237", "large242", "large254", "large259", "small35", "small186", "medium23", 
"medium139", "medium154", "medium158", "medium208", "medium246", "large26", "large39", "large56", "large77", "large164", "large220", "large232", "small11", "medium31", "medium56", "medium89", "medium172", "medium178", "medium180", "medium189", "medium212", "large21", "large27", "large51", "large55", "large74", "large92", "large93", "large112", "large135", "large143", "large152", "large167", "large196", "large199", "large207", "large210", "large212", "large251", "small97", "small144", "small223", "medium109", "medium133", "medium136", 
"medium170", "large5", "large12", "large44", "large52", "large65", "large85", "large86", "large106", "large133", "large139", "large165", "large168", "large174", "large187", "large189", "large195", "large205", "large233", "large247", "large255", "small2", "small23", "small24", "small46", "small65", "small71", "small72", "small106", "small109", "small141", "small152", "small194", "small211", "medium64", "medium141", "medium155", "medium161", "medium193", "medium207", "large8", "large22", "large50", "large57", "large82", "large88", "large89", "large101", "large126", "large158", "large161", "large172", "large176", "large188", "large190", "large221", "large238", "large250", "small105", "small113", "small173", "small202", "small224", "small244", "small257", "medium18", "medium143", "medium153", "medium186", "medium199", "large1", "large37", "large63", "large90", "large154", "large217", "large236", "small51", "small107", "small130", "small188", "small212", "small228", "small232", "small233", "small250", "medium2", "medium3", "medium22", "medium37", "medium51", "medium55", "medium57", "medium77", "medium179", "medium190", "large208", "large245", "large252", "small39", "small111", "small118", "small159", "medium38", "medium67", "medium126", "medium142", "medium173", "medium175", "medium223", "medium238", "large4", "large10", "large28", "large68", "large193", "small14", "small57", "small62", "small93", "small101", "small126", "small133", "small145", "small155", "small210", "small225", "small260", 
"medium49", "medium72", "medium76", "medium88", "medium144", "medium164", "medium177", "medium214", "large78", "large178", "large239", "large260", "small4", "small10", "small22", "small26", "small29", "small30", "small31", "small63", "small64", "small87", "small91", "small131", "small195", "small208", "small248", "medium4", "medium5", "medium7", "medium26", "medium29", "medium168", "medium194", "medium201", "medium220", "medium228", "medium250", "large76", "large170", "large211", "large224", "small8", "small19", "small25", "small52", 
"small54", "small68", "small73", "small88", "small95", "small102", "small112", "small127", "small128", "small163", "small165", "small201", "small204", "small251", "small253", "medium1", "medium27", "medium33", "medium44", "medium54", "medium68", "medium95", "medium124", "medium128", "medium157", "medium159", "medium182", "medium198", "medium202", "medium221", "medium226", "medium234", "large147", "large149", "large244", "large253", "small5", "small27", "small76", "small77", "small134", "small137", "small143", "small147", "small151", "small167", "small231", "small240", "small252", "small255", "medium9", "medium11", "medium19", "medium28", "medium34", "medium60", "medium73", "medium80", "medium82", "medium101", "medium106", "medium111", "medium137", "medium174", "medium195", "medium200", "medium203", "medium205", "medium219", "medium241", "medium247", "medium255", "medium257", "medium260", "large228", "small21", "small38", "small42", "small44", "small67", "small92", "small116", "small132", "small135", "small136", "small170", "small182", "small189", "small196", "small199", "small220", "small242", "medium12", "medium52", "medium116", "medium138", "medium151", "medium162", "medium188", "medium233", "medium242", "medium248", "medium251", "large136", "large159", "large173", "large179", "small34", "small48", "small61", "small82", "small124", "small157", "small174", "small175", "small178", 
"small187", "small190", "small214", "small237", "medium8", "medium20", "medium62", "medium92", "medium93", "medium113", "medium167", "medium169", "medium217", "medium252", "medium253", "large6", "large18", "small7", 
"small9", "small18", "small37", "small55", "small56", "small139", "small166", "small169", "small213", "small221", "small227", "medium59", "medium102", "medium112", "medium140", "medium150", "medium187", "medium213", 
"large151", "small1", "small28", "small89", "small168", "small193", "medium30", "medium48", "medium61", "medium74", "medium108", "medium134", "medium165", "medium196", "medium237", "large127", "large194", "small20", 
"small80", "small138", "small150", "small197", "small200", "small207", "small219", "small254", "medium131", 
"large175", "small74", "small205", "medium10", "medium135", "medium166", "large13", "large72", "large97", "large223", "small239", "medium71", "medium147", "medium118", "medium224", "medium240", "large61", "large119", "large246", "small185", "medium65", "medium163", "large20", "large213", "medium15", "medium39"};
int32_t len = 588;
int main(int argc, char* argv[]) {
    srand(time(0));
    std::string input_dir = "student_inputs/";
    std::string input_ext = ".in";
    std::string output_dir = "rpg_outputs/";
    std::string output_ext = ".out";
    std::string sizes[3] = {"small", "medium", "large"};
    int32_t lengths[3] = {100, 300, 1000};
    #pragma omp parallel
    {
        #pragma omp for
        for(int32_t num = 1; num < 261; num++){
            for(int32_t size = 0; size < 3; size++){
                // printf("making curr\n");
                std::string curr = sizes[size];
                curr = curr + std::to_string(num);
                // printf("Reading input\n");
                graph_t *G = read_input((input_dir + curr + input_ext).c_str(), lengths[size]);
                // printf("Starting next\n");
                auto[B, score] = test_on_all_k(G, 10000);
                printf("FINAL SCORE for %s OF %f\n", curr.c_str(), score);
                write_output(B, lengths[size], (output_dir + curr + output_ext).c_str());
                // printf("Wrote outputs\n");
                free_graph(G);
                free(B);
                // printf("Freed Graphs\n");
            }
        }
    }
    
    // for(int32_t i = 0; i < len; i ++){
    //     graph_t *G = read_input((input_dir + curr + input_ext).c_str(), lengths[size]);
    //     auto[B, score] = test_on_all_k(G, 5);
    //     printf("FINAL SCORE OF %f\n", score);
    //     write_output(B, lengths[size], (output_dir + curr + output_ext).c_str());
    //     free_graph(G);
    //     free(B);
    // }

    //run on specific
    // graph_t *G = read_input("student_inputs/medium1.in", 300);
    // auto[B, score] = test_on_all_k(G, 5);
    // printf("FINAL SCORE OF %f\n", score);
    // write_output(B, 300, "test.out");
    // free_graph(G);
    // free(B);
    return 0;
}