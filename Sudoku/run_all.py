import random
import sys
import pandas as pd

from solver_damion import *
from convert_sudoku import *


ALGORITHM = 'Normal DPLL'


sudoku_list = []

with open('sudokus/1000 sudokus.txt') as file:
    for line in file:
        line.rstrip()
        sudoku_list.append(line)

total_runtime = 0
total_success = 0
total_unit_clauses = 0

num_list = []
success_list = []
runtime_list = []


for line in  range(11): #range(len(sudoku_list)):
    convert_dimacs(sudoku_list[line])
    runtime, success, unit_clauses = run_sudoku()
    total_unit_clauses =+ unit_clauses
    total_runtime += runtime
    total_success += success

    num_list.append(line)
    success_list.append(success)
    runtime_list.append(runtime)

    print(f'Sudoku: {line + 1}, Numer of unit clauses: {total_unit_clauses}')
success_ratio = total_success / len(sudoku_list)
print(f'time: {total_runtime}, success = {total_success}')

sudokuframe = pd.DataFrame({'num':num_list, 'runtime':runtime_list, 'success': success_list})
sudokuframe.to_csv(f'{ALGORITHM}.csv')