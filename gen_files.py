from starter import *
from greedy import solver
import random

## INPUTS (PHASE 1)

MIN_TOTAL_WEIGHT = 500000

def gen_graph(n, debug=False, k=None):
    G = nx.empty_graph(n)
    if not k: k = random.choices(list(filter(lambda x: n % x == 0, range(4, 12))))[0]

    teams = [[] for _ in range(k)]
    for i, v in enumerate(random.sample(list(range(n)), n)):
        teams[i % k].append(v)
    
    num_edges = MAX_EDGES
    min_weight = 1 + MIN_TOTAL_WEIGHT // num_edges

    while num_edges > 0:
        allies = random.randint(0, k - 1)
        enemies = random.randint(0, k - 1)
        while enemies == allies:
            enemies = random.randint(0, k - 1)

        friend = random.choices(teams[allies])[0]
        foe = random.choices(teams[enemies])[0]

        if not G.has_edge(friend, foe):
            G.add_edge(friend, foe, weight = random.randint(min_weight, MAX_WEIGHT))
        
        num_edges -= 1
    
    O = G.copy()
    for i in range(k):
        for v in teams[i]:
            O.nodes[v]['team'] = i + 1
    
    visualize(O)

    if (debug):
        solved_greedily = solver(G.copy(), [team[0] for team in teams])
        print("Greedy:", score(solved_greedily))
        print("Optimal:", score(O))

        if score(O) != score(solved_greedily):
            visualize(solved_greedily)

    return G, O

def gen_graphs_for_phase_1():
    small_in, small_out = gen_graph(N_SMALL, k=10)
    medium_in, medium_out = gen_graph(N_MEDIUM, k=12)
    large_in, large_out = gen_graph(N_LARGE, k=10)

    write_input(small_in, 'inputs/small.in', overwrite=True)
    write_input(medium_in, 'inputs/medium.in', overwrite=True)
    write_input(large_in, 'inputs/large.in', overwrite=True)

    write_output(small_out, 'outputs/small.out', overwrite=True)
    write_output(medium_out, 'outputs/medium.out', overwrite=True)
    write_output(large_out, 'outputs/large.out', overwrite=True)

def check_graphs():
    def check_graph(i, o):
        G = read_input(i)
        validate_input(G)
        visualize(G)

        O = read_output(G, o)
        validate_output(O)
        visualize(O)

    check_graph('inputs/small.in', 'outputs/small.out')
    check_graph('inputs/medium.in', 'outputs/medium.out')
    check_graph('inputs/large.in', 'outputs/large.out')

## OUTPUTS (PHASE 2)

def gen_outputs(solver: solver, n: int, in_folder: str, out_folder: str, overwrite: bool = False, sizes = ('small', 'medium', 'large'), start = 1, finish = 261):
    for size in sizes:
        for n in range(start, finish):
            G = read_input(f'{in_folder}/{size}{n}.in')
            G = solver(G)
            print(f'{size}{n}: {score(G)}')
            write_output(G, f'{out_folder}/{size}{n}.out', overwrite=overwrite)

def target_output(solver: solver, in_file, out_file):
    print(f'Targeting {out_file}...')

    G = read_input(in_file)
    new = solver(G.copy())
    old = read_output(G.copy(), out_file)

    new_score = score(new)
    old_score = score(old)

    print(f'New score: {new_score}, Old score: {old_score}')
    if new_score < old_score:
        print(f'Saving new score {new_score}...')
        write_output(new, out_file, overwrite=True)
        print(f'Saved new score {new_score} to {out_file}!')
    else:
        print(f'Keeping old score {old_score}.')

# Import Library
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

# Returns a list of 
URL = 'https://170-leaderboard.vercel.app/team/thedegeneratecase'
def get_inputs_we_suck_on() -> list[str]:
    driver = webdriver.Chrome()
    driver.get(URL)
    soup = BeautifulSoup(driver.page_source,'html')
    driver.quit()
    tables = soup.find_all('table')
    items = []
    
    i = 0
    for table in tables:        
        items.append([
            [cell.text for cell in row.find_all(["th","td"])] 
            for row in table.find_all("tr")])
    # [... ['large 202', ' 68879.04259865842 ', ' 14 '] ...]
    def f(i):
        try:
            return int(i[2]) > 1
        except:
            return False
    items = filter(f, items[0])
    items = map(lambda i: ''.join(i[0].split(' ')), items)
    return items

# print(list(get_inputs_we_suck_on()))
inputs_to_improve = ['small1', 'small2', 'small3', 'small4', 'small5', 'small7', 'small8', 'small9', 'small10', 'small11', 'small12', 'small13', 'small14', 'small15', 'small18', 'small19', 'small20', 'small21', 'small22', 'small23', 'small24', 'small25', 'small26', 'small27', 'small28', 'small29', 'small30', 'small31', 'small34', 'small35', 'small37', 'small38', 'small39', 'small42', 'small44', 'small46', 'small47', 'small48', 'small51', 'small52', 'small54', 'small55', 'small56', 'small57', 'small58', 'small61', 'small62', 'small63', 'small64', 'small65', 'small67', 'small68', 'small70', 'small71', 'small72', 'small73', 'small74', 'small76', 'small77', 'small79', 'small80', 'small82', 'small83', 'small84', 'small87', 'small88', 'small89', 'small91', 'small92', 'small93', 'small94', 'small95', 'small97', 'small99', 'small101', 'small102', 'small103', 'small105', 'small106', 'small107', 'small108', 'small109', 'small111', 'small112', 'small113', 'small114', 'small115', 'small116', 'small118', 'small123', 'small124', 'small125', 'small126', 'small127', 'small128', 'small129', 'small130', 'small131', 'small132', 'small133', 'small134', 'small135', 
'small136', 'small137', 'small138', 'small139', 'small141', 'small143', 'small144', 'small145', 'small146', 'small147', 'small150', 'small151', 'small152', 'small154', 'small155', 'small156', 'small157', 'small158', 'small159', 'small160', 'small162', 'small163', 'small165', 'small166', 'small167', 'small168', 'small169', 'small170', 'small172', 'small173', 'small174', 'small175', 'small176', 'small177', 'small178', 'small180', 'small182', 'small184', 'small185', 'small186', 'small187', 'small188', 'small189', 'small190', 'small192', 'small193', 'small194', 'small195', 'small196', 'small197', 'small199', 'small200', 'small201', 'small202', 'small204', 'small205', 'small207', 'small208', 'small210', 'small211', 'small212', 'small213', 'small214', 'small215', 'small219', 'small220', 'small221', 'small223', 'small224', 'small225', 'small226', 'small227', 'small228', 'small229', 'small231', 'small232', 'small233', 'small235', 'small236', 'small237', 'small238', 'small239', 'small240', 'small242', 'small243', 'small244', 'small245', 'small248', 'small249', 'small250', 'small251', 'small252', 'small253', 'small254', 'small255', 'small257', 'small259', 'small260', 'medium1', 'medium2', 'medium3', 'medium4', 'medium5', 'medium7', 'medium8', 'medium9', 'medium10', 'medium11', 'medium12', 'medium13', 'medium14', 'medium15', 'medium18', 'medium19', 'medium20', 'medium21', 'medium22', 'medium23', 'medium25', 'medium26', 'medium27', 'medium28', 'medium29', 'medium30', 'medium31', 'medium33', 'medium34', 'medium37', 'medium38', 'medium39', 'medium41', 'medium42', 'medium44', 'medium47', 'medium48', 'medium49', 'medium50', 'medium51', 'medium52', 'medium53', 'medium54', 'medium55', 'medium56', 'medium57', 'medium59', 'medium60', 'medium61', 'medium62', 'medium63', 'medium64', 'medium65', 'medium66', 'medium67', 'medium68', 'medium69', 'medium70', 'medium71', 'medium72', 'medium73', 'medium74', 'medium76', 'medium77', 'medium78', 'medium79', 'medium80', 'medium82', 'medium83', 'medium84', 'medium85', 'medium87', 
'medium88', 'medium89', 'medium92', 'medium93', 'medium94', 'medium95', 'medium97', 'medium98', 'medium99', 'medium101', 'medium102', 'medium103', 'medium106', 'medium107', 'medium108', 'medium109', 'medium111', 'medium112', 'medium113', 'medium115', 'medium116', 'medium118', 'medium119', 'medium123', 'medium124', 'medium126', 'medium127', 'medium128', 'medium129', 'medium132', 
'medium133', 'medium134', 'medium135', 'medium136', 'medium137', 'medium138', 'medium139', 'medium140', 'medium141', 'medium142', 'medium143', 'medium144', 'medium146', 'medium147', 'medium148', 'medium150', 'medium151', 'medium152', 'medium153', 'medium154', 'medium155', 'medium156', 'medium157', 'medium158', 'medium159', 'medium160', 'medium161', 'medium162', 'medium163', 'medium164', 'medium165', 'medium166', 'medium167', 'medium168', 'medium169', 'medium170', 'medium172', 'medium173', 'medium174', 'medium175', 'medium176', 'medium177', 'medium178', 'medium179', 'medium180', 'medium182', 'medium184', 'medium185', 'medium186', 'medium187', 'medium188', 'medium189', 'medium190', 'medium192', 'medium193', 'medium194', 'medium195', 'medium196', 'medium197', 'medium198', 'medium199', 'medium200', 'medium201', 'medium202', 'medium203', 'medium205', 'medium207', 'medium208', 'medium210', 'medium212', 'medium213', 'medium214', 'medium215', 'medium217', 'medium219', 'medium220', 'medium221', 'medium223', 'medium224', 'medium225', 'medium226', 'medium227', 'medium228', 'medium229', 'medium230', 'medium232', 'medium233', 'medium234', 'medium236', 'medium237', 'medium238', 'medium239', 'medium240', 'medium241', 'medium242', 'medium244', 'medium246', 'medium247', 'medium248', 'medium249', 'medium250', 'medium251', 'medium252', 'medium253', 'medium254', 'medium255', 'medium256', 'medium257', 'medium259', 'medium260', 'large1', 'large2', 'large3', 'large4', 'large5', 'large6', 'large7', 'large8', 'large9', 'large10', 'large11', 'large12', 'large13', 'large14', 'large17', 'large18', 'large20', 'large21', 'large22', 'large23', 'large25', 'large26', 'large27', 'large28', 'large29', 'large31', 'large32', 'large33', 'large34', 'large37', 'large38', 'large39', 'large42', 'large44', 'large47', 'large48', 'large49', 'large50', 'large51', 'large52', 'large53', 'large54', 'large55', 'large56', 
'large57', 'large58', 'large59', 'large60', 'large62', 'large63', 'large64', 'large65', 'large67', 'large68', 'large69', 'large70', 'large72', 'large73', 'large74', 'large76', 'large77', 'large78', 'large80', 'large82', 'large83', 'large84', 'large85', 'rge112', 'large114', 'large117', 'large119', 'large120', 'large122', 'large123', 'large124', 'large126', 'large127', 'large128', 'large129', 'large131', 'large133', 'large135', 'large136', 'large137', 'large138', 'large139', 'large140', 'large141', 'large143', 'large144', 'large145', 'large146', 'large147', 'large149', 'large150', 'large151', 'large152', 'large154', 'large155', 
'large157', 'large158', 'large159', 'large160', 'large161', 'large162', 'large163', 'large164', 'large165', 'large167', 'large168', 'large169', 'large170', 'large172', 'large173', 'large174', 'large175', 'large176', 'large177', 'large178', 'large179', 'large180', 'large182', 'large184', 'large186', 'large187', 'large188', 'large189', 'large190', 'large192', 'large193', 'large194', 'large195', 'large196', 'large197', 'large198', 'large199', 'large200', 'large201', 'large202', 'large205', 'large206', 'large207', 'large208', 'large209', 'large210', 'large211', 'large212', 'large213', 'large214', 'large215', 'large216', 'large217', 'large218', 'large219', 'large220', 'large221', 'large223', 'large224', 'large225', 'large227', 'large228', 'large229', 'large230', 'large232', 'large233', 'large234', 'large235', 'large236', 'large237', 'large238', 'large239', 'large241', 'large242', 'large244', 'large245', 'large246', 'large247', 'large248', 'large249', 'large250', 'large251', 'large252', 'large253', 'large254', 'large255', 'large257', 'large258', 'large259', 'large260']

#v isualize(read_input('student_inputs/large53.in'))
# visualize(read_output(read_input('student_inputs/large53.in'), 'rpg_outputs/large53.out'))

def tar_best(destination: str, input: str, outputs: list[str], overwrite=True):
    for size in ['small', 'medium', 'large']:
        for n in range(1, 261):
            G = read_input(f'{input}/{size}{n}.in')
            read_G = lambda p: read_output(G.copy(), p)
            solutions = map(lambda p: f'{p}/{size}{n}.out', outputs)
            solutions = filter(os.path.exists, solutions)
            solutions = map(read_G, solutions)
            G = min(solutions, key=score)
            print(f'Best solution for {size}{n}: {score(G)}')
            write_output(G, f'{destination}/{size}{n}.out', overwrite=overwrite)

    tar(destination, overwrite=overwrite)

tar_best('out', 'student_inputs', [f'rpg_outputs_{x}' for x in ['a', 'b','c']])
