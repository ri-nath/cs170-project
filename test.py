from starter import *
from typing import Callable

EXAMPLE_IN = 'inputs/example.in' # Temporary
EXAMPLE_OUT = 'outputs/example.out' # Temporary

solver = Callable[[nx.Graph], nx.Graph]

def test_vs_output(solver: solver, in_file: str = EXAMPLE_IN, out_file: str = EXAMPLE_OUT):
    G = read_input(in_file)

    solved = solver(G.copy())
    optimal = read_output(G.copy(), out_file)

    solved_score = score(solved, separated=True)
    optimal_score = score(optimal, separated=True)
    print(f'Score of solver on {in_file}:', ' + '.join(map(str, solved_score)), '=', sum(solved_score))
    print(f'Score of {out_file} on {in_file}:', ' + '.join(map(str, optimal_score)), '=', sum(optimal_score))
    visualize(solved)

def test_on_input(solver: solver, in_file: str = EXAMPLE_IN):
    G = read_input(in_file)

    solved = solver(G.copy())

    solved_score = score(solved, separated=True)
    print(f'Score of solver on {in_file}:', ' + '.join(map(str, solved_score)), '=', sum(solved_score))
    visualize(solved)

def test_on_graph(solver: solver, G: nx.Graph):
    solved = solver(G)
    solved_score = score(solved, separated=True)
    print(f'Score of solver:', ' + '.join(map(str, solved_score)), '=', sum(solved_score))
    visualize(solved)

def test_on_simple_graph(solver: solver, weight: int = 100, width: int = 3, height: int = 2):
    G = nx.empty_graph(width * height)
    for i in range(width * height):
        if i < width * (width - 1):
            G.add_edge(i, i + width, weight=weight)
        if i + 1 % width != 0:
            G.add_edge(i, i + 1, weight=weight)

    test_on_graph(solver, G)

def gen_outputs(solver: solver, n: int, in_folder: str, out_folder: str, overwrite: bool = False, sizes = ('small', 'medium', 'large'), start = 1, finish = 261):
    for size in sizes:
        for n in range(start, finish):
            G = read_input(f'{in_folder}/{size}{n}.in')
            G = solver(G)
            print(f'{size}{n}: {score(G)}')
            write_output(G, f'{out_folder}/{size}{n}.out', overwrite=overwrite)