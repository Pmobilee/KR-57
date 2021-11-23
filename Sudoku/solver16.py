# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 14:48:51 2021

@author: Pablo
"""

import random
import sys
import time


# def load_txt16(file): # transform a sudoku into cnf - can generalize this method by adding a dimension param for the 'for' loop
#     f = open(file, 'r')
#     data = f.readline()
#     f.close()
#     cnf = []
#     for i in range(1, 17):
#         for j in range(1, 17):        
#             if data[0] != '.':                
#                 if (data[0] == 'G'):
#                     d = 16
#                 else:
#                     d = int(data[0], 16)
#                 cnf.append([i*17*17 + j*17 + d])
#             #print(i, j)
#             #print(i*17*17 + j*17 + d)
#             data = data[1:]
#     return cnf

def load_txt16(data): # transform a sudoku into cnf - can generalize this method by adding a dimension param for the 'for' loop
    cnf = []
    for i in range(1, 17):
        for j in range(1, 17):        
            if data[0] != '.':                
                if (data[0] == 'G'):
                    d = 16
                else:
                    d = int(data[0], 16)
                cnf.append([i*17*17 + j*17 + d])
            #print(i, j)
            #print(i*17*17 + j*17 + d)
            data = data[1:]
    return cnf

def load_dimacs(file):
    f = open(file, 'r') # open file in reading mode
    data = f.read() # read file in data variable; string type
    f.close()
    lines = data.split("\n") # split the data into a list of lines
    cnf = []
    for line in lines:
        if len(line) == 0 or line[0] in ['c', 'p', '%', '0']:
            continue # ignore the lines without clauses
        clause = [int(x) for x in line.split()[:-1]] # transform the string clause format into a int one, remove the last 0;
        cnf.append(clause) # add the clause to the list
    return cnf


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

count = 0

def unit_propagation(formula):
    assignment = []
    unit_clauses = []
    for clause in formula:
        if len(clause) == 1:
            unit_clauses.append(clause)

    while unit_clauses:
        global count
        count += 1
    
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
    counted_literals = dict_literal(formula)
    variable = list(counted_literals)[0]
    potential_assignment = assignment + [variable]
    solution = dpll(boolean_constraint_propagation(formula, variable), potential_assignment)

    # if literal assignment of chosen variable did not satisfy then try -assignment for the variable
    if not solution:
        potential_assignment = assignment + [-variable]
        solution = dpll(boolean_constraint_propagation(formula, -variable), potential_assignment)

    return solution


def run_sudoku(cnf):
    start_time = time.time()
    solution = dpll(cnf, [])
    end_time =  time.time() - start_time
    global count
    
    if solution:
        solution.sort(key=abs)
        #print(solution)
        #print(len(solution))
        # write_sudoku(solution)
        #solution needs to be written to a file with name filein.out
        # print(f'Number of unit clauses: {count}')
        success = 1
    else:
        success = 0
    
    unit_clauses = count
    count = 0
    return end_time, success, unit_clauses


# need to write a main works with "command SAT -Sn inputfile , for example: SAT -S2 sudoku_nr_10 , where SAT is the (compulsory) name of your program,
# n=1 for the basic DP and n=2 or 3 for your two other strategies, and the input file is the concatenation of all required input clauses
# (in your case: sudoku rules + given puzzle).

total_runtime = 0
total_success = 0
total_unit_clauses = 0

num_list = []
success_list = []
runtime_list = []

sudoku_list = []

with open('C:/Users/Pablo/Desktop/Pablo/knowledge representation/project1/SudokuSATSolver-main/SudokuSATSolver-main/test sudokus/16x16.txt') as file:
    for line in file:
        line.rstrip()
        sudoku_list.append(line)
        
for i in range(10):
    sudoku = load_txt16(sudoku_list[i])
    rules = load_dimacs('C:/Users/Pablo/Desktop/Pablo/knowledge representation/project1/SudokuSAT/SudokuSAT/sat_tests/sudoku_dimacs/sudoku-rules-16x16.txt')
    cnf = sudoku + rules
    
    
    runtime, success, unit_clauses = run_sudoku(cnf)
    total_unit_clauses =+ unit_clauses
    total_runtime += runtime
    total_success += success

    num_list.append(line)
    success_list.append(success)
    runtime_list.append(runtime)

    success_ratio = total_success / len(sudoku_list)
print('Time elapsed: ',total_runtime , 'Success: ', total_success)

