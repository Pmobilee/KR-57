import random
import sys
import time

start = time.time()

num_variables = int()
num_clauses = int()


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


# def dict_literal(formula):
#     dict = {}
#     for clause in formula:
#         for literal in clause:
#             if literal in dict:
#                 dict[literal] += 1
#             else:
#                 dict[literal] = 1
#     return dict

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
#    out = []
    for clause in formula:
        if unit in clause:
#            out.append(clause)
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

def dpll(formula, assignment):
    #pure_literal has to be implemented



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

    #choose which variable should be explored first (no heuristic yet) creates a dictionary with key = literal and value = counted times in formula
    variable = mom(formula)
    potential_assignment = assignment + [variable]
    solution = dpll(boolean_constraint_propagation(formula, variable), potential_assignment)

    # if literal assignment of chosen variable did not satisfy then try -assignment for the variable
    if not solution:
        potential_assignment = assignment + [-variable]
        solution = dpll(boolean_constraint_propagation(formula, -variable), potential_assignment)

    return solution

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

end = time.time()
print('\n\nTime elapsed: ', end - start, 'seconds')

# need to write a main works with "command SAT -Sn inputfile , for example: SAT -S2 sudoku_nr_10 , where SAT is the (compulsory) name of your program,
# n=1 for the basic DP and n=2 or 3 for your two other strategies, and the input file is the concatenation of all required input clauses
# (in your case: sudoku rules + given puzzle).



