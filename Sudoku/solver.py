import random
import sys
import time

num_variables = int()
num_clauses = int()
backtrack = 0


def write_sudoku(solution):
    new= []
    for assignment in solution:
        if assignment < 0:
            continue
        new.append(assignment)
    col = 1
    for assignment in new:
        if col == 10:
            print("")
            col = 1
        print(f"{assignment % 10} ", end='')
        col += 1


def dict_literal(formula):
    dict = {}
    for clause in formula:
        for literal in clause:
            if literal in dict:
                dict[literal] += 1
            else:
                dict[literal] = 1
    return dict

def dlis(formula):
    dict = dict_literal(formula)
    dict = sorted(dict.items(), key=lambda x: x[1], reverse=True)
    return dict

def jeroslow(formula):
    dict = {}
    for clause in formula:
        for literal in clause:
            if literal in dict:
                dict[literal] += 2^(-abs(len(clause)))
            else:
                dict[literal] = 2^(-abs(len(clause)))
    dict = sorted(dict.items(), key=lambda x: x[1], reverse=True)
    return dict

def mom(formula):
    min_len = min(map(len, formula))
    app = {}
    for clause in formula:
        if len(clause) == min_len:
            for literal in clause:
                if literal in app:
                    app[literal] += 1
                else:
                    app[literal] = 1
    mom_value_max = 0
    keys = app.keys()
    for i in keys:
        try:
            mom_value_new = (app.get(i) + app.get(-i))*2 + app.get(i) + app.get(-i)
            if mom_value_new > mom_value_max:
                mom_value_max = mom_value_new
                mom_best = i
        except:
            continue
    return mom_best

def heuristics_dict(heuristic):
    heuristics = {
        'S'    : jeroslow_wang,
        'S2'   : random_selection,
        'S3'    : most_often,
    }
    try:
        return heuristics[heuristic]
    except:
        sys.exit("ERROR: '{}' Not valid heuristic.".format(heuristic) +
                 "\nValid heuristics: {}".format(heuristics.keys()))

def parse(filename):
    clauses = []
    for line in open(filename):
        if line.startswith('c'):
            continue
        if line.startswith('p'):
            n_vars = line.split()[2]
            num_clauses= line.split()[3]
            continue
        clause = [int(x) for x in line[:-2].split()]
        clauses.append(clause)
    return clauses, int(n_vars), int(num_clauses)

def boolean_constraint_propagation(formula, unit):
    modified = []
    for clause in formula:
        if unit in clause:
            continue
        if -unit in clause:
            new_clause = [x for x in clause if x != -unit]
            if not new_clause:
                return -1
            modified.append(new_clause)
        else:
            modified.append(clause)
    return modified

def unit_propagation(formula):
    assignment = []
    unit_clauses = []
    for clause in formula:
        if len(clause) == 1:
            unit_clauses.append(clause)

    while unit_clauses:
        unit = unit_clauses[0]
        formula = boolean_constraint_propagation(formula, unit[0])
        assignment += [unit[0]]
        if formula == -1:
            return -1, []
        if not formula:
            return formula, assignment
        unit_clauses = []
        for clause in formula:
            if len(clause) == 1:
                unit_clauses.append(clause)
    return formula, assignment


def pure_(formula):
    dict= dict_literal(formula)
    keys = dict.keys()
    pures = []
    assignment = []
    for key in keys:
        if -key in keys:
            continue
        else:
            pures.append(key)
    while pures:
        pure = pures[0]
        formula = boolean_constraint_propagation(formula, pures[0])
        assignment += [pure[0]]
        if formula == -1:
            return -1, []
        if not formula:
            return formula, assignment
        pures = []
        for key in keys:
            if -key in keys:
                continue
            else:
                pures.append(key)
    return formula, assignment

def dpll(formula, assignment):

    #unit_clauses
    formula, unit_assignment = unit_propagation(formula)
    #add all assignment from unit_clauses to solution assignment
    assignment = assignment + unit_assignment
    #if bcp found inconsistency, variable assignment is not an potential solution
    if formula == - 1:
        return []

    #if all clauses satisfied
    if not formula:
        return assignment

    formula, pure_assign = pure_(formula)
    assignment = assignment + pure_assign
    #if bcp found inconsistency, variable assignment is not an potential solution
    if formula == - 1:
        return []

    #if all clauses satisfied
    if not formula:
        return assignment

    #choose which variable should be explored first (no heuristic yet) creates a dictionary with key = literal and value = counted times in formula
    counted_literals = dict_literal(formula)
    variable = list(counted_literals)[0]
    potential_assignment = assignment + [variable]
    solution = dpll(boolean_constraint_propagation(formula, variable), potential_assignment)

    # if literal assignment of chosen variable did not satisfy then try -assignment for the variable
    if not solution:
        global backtrack
        backtrack += 1
        potential_assignment = assignment + [-variable]
        solution = dpll(boolean_constraint_propagation(formula, -variable), potential_assignment)

    return solution


def run_sudoku(cnf):
    start_time = time.time()
    solution = dpll(cnf, [])
    end_time = time.time() - start_time
    global count
    global backtrack
    if solution:
        solution.sort(key=abs)
        # write_sudoku(solution)
        success = 1
    else:
        success = 0

    unit_clauses = count
    backtrack_number = backtrack
    count = 0
    backtrack = 0
    return end_time, success, unit_clauses, backtrack_number

cnf, num_variables, num_clauses = parse('sudoku-combined.txt')
solution = dpll(cnf, [])

if solution:
    solution.sort(key=abs)
    #print(solution)
    #print(len(solution))
    write_sudoku(solution)
    #solution needs to be written to a file with name filein.out
else:
    print('UNSATISFIABLE')