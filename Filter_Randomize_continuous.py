import csv

allowed_nums=[]
with open('testing_run-num.txt') as file:
	for line in file:
		allowed_nums.append(int(line.split('\n')[0]))

n=0
Data=[[], []]
with open('2022-07-06_Preempt-Input-Matrix_continuous.csv') as file:
	for line in file:
		n+=1
		if n==1:
			continue
		f=line.split('\n')[0].split(',')
		Data[int(int(f[0]) in allowed_nums)].append(f[1:])

with open('2022-07-06_Preempt-Input-Matrix_training_continuous.csv', "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(Data[0])

with open('2022-07-06_Preempt-Input-Matrix_testing_continuous.csv', "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(Data[1])
