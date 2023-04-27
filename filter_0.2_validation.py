from random import random
import numpy as np 
run_num=[]
rand_num=[]

all_runs=set(list(range(1, 161)))

with open('testing_run-num.txt') as outfile:
	for line in outfile:
		all_runs.remove(int(line.split('\n')[0]))

all_runs=sorted(list(all_runs))
all_runs=[str(1000+i)[1:] for i in all_runs]

rand_num=[]
for i in all_runs:
	rand_num.append(random())

limit=np.percentile(rand_num, 25)

with open('validation_run-num.txt', 'w+') as outfile:
    for i in range(len(rand_num)):
        if rand_num[i]<limit:
            outfile.write(all_runs[i]+'\n')
   
with open('training_run-num.txt', 'w+') as outfile:
    for i in range(len(rand_num)):
        if rand_num[i]>=limit:
            outfile.write(all_runs[i]+'\n')           
