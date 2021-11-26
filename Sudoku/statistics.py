import statistics
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from scipy import stats


def plot_boxplots_runtime(DPLL, MOM, JW, size, metric):

    # Here, I'm going to do a lot of extra work to specifically calculate the means of the mean of all runs. his is because
    # It's specifically stated in the assignment, and perhaps this leads to different boxplots compared to cal. it directly

    
    runtime_dpll = []
    runtime_MOM = []
    runtime_JW = []

    count_dpll = 0
    count_mom = 0
    count_jw = 0

    for i in range(len(DPLL['success'])):
        if DPLL['success'][i] == '0':
            
            continue
        else: runtime_dpll.append(DPLL[f'{metric}'][i])
    
    for i in range(len(MOM[f'success'])):
        if MOM['success'][i] == '0' :
            
            continue
        else: runtime_MOM.append(MOM[f'{metric}'][i])
        
    for i in range(len(JW[f'success'])):
        if JW['runtime'][i] :
            
            continue

        else: runtime_JW.append(JW[f'{metric}'][i])
        

    # for counting:

    # for i in range(len(DPLL['runtime'])):
    #     if DPLL['runtime'][i] > 250.0:
    #         count_dpll += 1
            
    
    # for i in range(len(MOM[f'runtime'])):
    #     if MOM['runtime'][i] > 250.0:
    #         count_mom += 1
            
        
        
    # for i in range(len(JW[f'runtime'])):
    #     if JW['runtime'][i] > 250.0:
    #         count_jw += 1
            

    runtime_dpll = DPLL[f'{metric}']
    runtime_MOM = MOM[f'{metric}']
    runtime_JW = JW[f'{metric}']

    
    print(f'dpll: {count_dpll}, mom: {count_mom}, jw: {count_jw}')

    fig1, ax1 = plt.subplots()
    ax1.boxplot([runtime_dpll, runtime_MOM, runtime_JW], labels =('DPLL', 'MOM', 'JW'))
    #ax1.set_aspect(0.01, 0.01)
    if metric == 'runtime':
        plt.ylabel('runtime (s)')
        plt.ylim(0, 250)
    elif metric == 'number of backtracks':
        plt.ylabel('backtracks (n)')
        # plt.ylim(-4, 4)
    plt.suptitle(f'{size} sudoku')
    plt.savefig(f'D:/OneDrive/Desktop/STATISTICS/{size}_{metric}_boxplot.png')
    # plt.show()


DPLL = pd.read_csv('D:/OneDrive/Desktop/STATISTICS/DPLL.csv')
MOM = pd.read_csv('D:/OneDrive/Desktop/STATISTICS/MOM.csv')
JW = pd.read_csv('D:/OneDrive/Desktop/STATISTICS/Jeroslow.csv')

# print(DPLL['runtime'])
size = '16x16'

plot_boxplots_runtime(DPLL, MOM, JW, size , metric = 'runtime')
plot_boxplots_runtime(DPLL, MOM, JW, size, metric = 'number of backtracks')

print(f'\n\nSudocu size: {size}\n')


dpll_runtime = []
dpll_success = list(DPLL['success'])
dpll_backtracks = []

MOM_runtime = []
MOM_success = list(MOM['success'])
MOM_backtracks = []

JW_runtime = []
JW_success = list(JW['success'])
JW_backtracks = []



for i in range(len(DPLL['success'])):
    if DPLL['success'][i] == '0':
        continue
    else: 
        dpll_runtime.append(DPLL['runtime'][i])
        dpll_backtracks.append(DPLL['number of backtracks'][i])

for i in range(len(MOM[f'success'])):
    if MOM['success'][i] == '0':
        continue
    else: 
        MOM_runtime.append(MOM['runtime'][i])
        MOM_backtracks.append(MOM['number of backtracks'][i])
    
for i in range(len(JW['success'])):
    if JW['success'][i] == '0':
        continue
    else: 
        
        JW_runtime.append(JW['runtime'][i])
        JW_backtracks.append(JW['number of backtracks'][i])

A = pd.DataFrame({'dpll_runtime' : dpll_runtime, 'dpll_backtracks' : dpll_backtracks, 'MOM_runtime' : MOM_runtime, 'MOM_backtracks':MOM_backtracks, 'JW_runtime' : JW_runtime, 'JW_backtracks' : JW_backtracks})

dpll_runtime = A['dpll_runtime']
dpll_backtracks = A['dpll_backtracks']
MOM_runtime = A['MOM_runtime']
MOM_backtracks = A['MOM_backtracks']
JW_runtime = A['JW_runtime']
JW_backtracks = A['JW_backtracks']


print(f'DPLL runtime mean: {dpll_runtime.mean()} median: {dpll_runtime.mean()}, max: {dpll_runtime.mean()}, min: {dpll_runtime.mean()}')
print(f'DPLL backtracks mean: {dpll_backtracks.mean()} median: {dpll_backtracks.median()}, max: {dpll_backtracks.max()}, min: {dpll_backtracks.min()}')
print(f'Succes/Total ratio: {dpll_success.count(1)}/{len(dpll_success)}')


print(f'MOM runtime mean: {MOM_runtime.mean()} median: {MOM_runtime.median()}, max: {MOM_runtime.max()}, min: {MOM_runtime.min()}')
print(f'MOM backtracks mean: {MOM_backtracks.mean()} median: {MOM_backtracks.median()}, max: {MOM_backtracks.max()}, min: {MOM_backtracks.min()}')
print(f'Succes/Total ratio: {MOM_success.count(1)}/{len(MOM_success)}')



print(f'JW runtime mean: {JW_runtime.mean()} median: {JW_runtime.median()}, max: {JW_runtime.max()}, min: {JW_runtime.min()}')
print(f'JW backtracks mean: {JW_backtracks.mean()} median: {JW_backtracks.median()}, max: {JW_backtracks.max()}, min: {JW_backtracks.min()}')
print(f'Succes/Total ratio: {JW_success.count(1)}/{len(JW_success)}')

print(f'\nStatistics:\n')

print('Runtime:')
print(f'DPLL vs MOM: {stats.ttest_ind(dpll_runtime, MOM_runtime)}')
print(f'DPLL vs JW: {stats.ttest_ind(dpll_runtime, JW_runtime)}')
print(f'MOM vs JW: {stats.ttest_ind(MOM_runtime, JW_runtime)}')

list_mean_dpll = [0.00268, 0.68189, 154.129]
list_mean_mom = [0.002696, 0.6501, 72.5721]
list_mean_jw = [0.00268991152, 0.709853, 159.55735]
list_gens = ['4x4', "9x9", "16x16"]


plt.plot(list_gens,list_mean_dpll, 'g', label="DPLL")
plt.plot(list_gens,list_mean_mom,'b' , label="MOM")
plt.plot(list_gens,list_mean_jw,'r' , label="Jeroslow-Wang")


plt.legend(['DPLL', 'MOM', 'Jeroslow-Wang'], loc='lower right')
plt.ylabel('runtime')
plt.xlabel('Sudoku size')
plt.yscale('log')
# plt.suptitle('Generational Fitness GA vs DE')
plt.xticks(np.arange(0, 3, 1))
plt.savefig('runtime_log.png')
plt.show()
