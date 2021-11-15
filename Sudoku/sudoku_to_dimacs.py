from numpy import sqrt

file = ".94...13..............76..2.8..1.....32.........2...6.....5.4.......8..7..63.4..8"

variables_no = int(sqrt(len(file)))
variables = []

#this seems like too much code for what it does, maybe because I work with it as a string, which is necessary for line 20
for x in range(variables_no):
    x +=1
    variables.append(f"{x}")

col = 1
row = 1
result = []
for symbol in file:
    if col == (variables_no+1):
        row += 1
        col = 1
    if symbol in variables:
        result.append(f"{row}{col}{symbol} 0")
    col += 1

variables_dimacs = []
for clause in result:
    if clause[:-2] in variables_dimacs:
        continue
    variables_dimacs.append(clause)


with open('sudoku-rules.txt', 'r') as f:
    data = f.read().splitlines()
    data1 = data[1:]


with open('sudoku-example.txt', 'w') as f:
    f.write(f"p cnf {variables_dimacs} {len(result)} \n")
    for line in result:
        f.write(line)
        f.write('\n')

data1+= result

with open('sudoku-combined.txt', 'w') as fp:
    fp.write(f"p cnf 729 {len(data) + len(result)-1 } \n")
    for line in data1:
        fp.write(line)
        fp.write('\n')






