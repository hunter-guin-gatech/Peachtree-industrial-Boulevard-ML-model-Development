from bisect import bisect 
import csv

def projectDist(trajdist, trajtime, T):
    j=bisect(trajtime, T)
    if j==0:
        k, k1=0, 1
    else:
        k, k1=j-1, j

    return trajdist[k]+(trajdist[k1]-trajdist[k])/(trajtime[k1]-trajtime[k])*(T-trajtime[k])

cutoffs=[0.8, 0.85, 0.9, 0.95]
for cutoff in cutoffs:
    n=0
    Data=[['SimNum','Time', 'Distance']]
    for i in range(-159, 1):
        Data[0].append('det10_'+str(i))
    for i in range(-159, 1):
        Data[0].append('det12_'+str(i))
    for i in range(-159, 1):
        Data[0].append('left10_'+str(i))
    for i in range(-159, 1):
        Data[0].append('through10_'+str(i))
    for i in range(-159, 1):
        Data[0].append('left12_'+str(i))
    for i in range(-159, 1):    
        Data[0].append('through12_'+str(i))
    Data[0].extend(['Preempt-Decision-Linear', 'Preempt-Decision-NegExp', 'Preempt-Decision-PosExp'])

    with open('1_PreemptSummary_12NB-13NB-15NB-16NB-18NB-19NB-20NB.csv') as file:
        for line in file:
            n+=1
            f=line.split('\n')[0].split(',')
            if n==1:
                continue
            simNum=str(1000+int(f[0]))[1:]
            print(simNum)
            preemptTime=int(float(f[3]))
            signalList=[]
            entryTime=((int(f[0])-1)%32)*5+3522.5

            trajdist=[0]; trajtime=[0]
            with open('../../../2022-05-09_PIB-Mainline-Prediction-Model-Development/1_Trajectory_Plots/TrajectoryData/2022-06-08_PIB-RBC-Preempt-Trajectory_'+simNum+'_Optimal-Solution-1.csv') as trajfile:
                for trajline in trajfile:
                    g=trajline.split('\n')[0].split(',')
                    try:
                        t, Vtype, dist=round((float(g[1])-entryTime)*10)/10, int(g[3]), float(g[2])
                        if Vtype==630:
                            if trajtime[-1]<t:
                                trajdist.append(dist)
                                trajtime.append(t)
                    except (ValueError, IndexError):
                        continue               

            det10=[]
            with open('../../../2022-05-09_PIB-NB-ERV-Solution-Effort/12NB_1/OutputFiles/Final-Preempt-Run/2022-05-09_CTEDD_Peachtree-Industrial-Blvd-RBC-P_NE_10_'+simNum+'.ldp') as detfile:
                for detline in detfile:
                    g=detline.split('\n')[0].split()
                    try:
                        t=float(g[0][:-2])
                        d1, d2=g[0][-2:]
                        det10.append([t, int(d1=='+')+int(d2=='+')])            
                    except (ValueError, IndexError):
                        continue

            det12=[]
            with open('../../../2022-05-09_PIB-NB-ERV-Solution-Effort/12NB_1/OutputFiles/Final-Preempt-Run/2022-05-09_CTEDD_Peachtree-Industrial-Blvd-RBC-P_NE_12_'+simNum+'.ldp') as detfile:
                for detline in detfile:
                    g=detline.split('\n')[0].split()
                    try:
                        t=float(g[0][:-2])
                        d1, d2=g[0][-2:]
                        det12.append([t, int(d1=='+')+int(d2=='+')])
                    except (ValueError, IndexError):
                        continue


            left10=[[0, 0]]; through10=[[0, 0]]; left12=[[0, 0]]; through12=[[0, 0]]
            with open('../../../2022-05-09_PIB-NB-ERV-Solution-Effort/12NB_1/OutputFiles/Final-Preempt-Run/2022-05-09_CTEDD_Peachtree-Industrial-Blvd-RBC-P_NE_'+simNum+'.lsa') as sigfile:
                for sigline in sigfile:
                    g=sigline.split('\n')[0].split(';')
                    try:
                        t, ph, state=int(float(g[0])), str(int(g[2]))+'-'+str(int(g[3])), ''.join(g[4].split())
                        statenum=1 if state=='green' else (0 if state=='red' else 2)
                        if ph=='10-1':
                            prevtime, prevstate=left10[-1]
                            for i in range(prevtime+1, t):
                                left10.append([i, prevstate])
                            left10.append([t, statenum])
                        elif ph=='12-1':
                            prevtime, prevstate=left12[-1]
                            for i in range(prevtime+1, t):
                                left12.append([i, prevstate])
                            left12.append([t, statenum])
                        elif ph=='10-6':
                            prevtime, prevstate=through10[-1]
                            for i in range(prevtime+1, t):
                                through10.append([i, prevstate])
                            through10.append([t, statenum])
                        elif ph=='12-6':
                            prevtime, prevstate=through12[-1]
                            for i in range(prevtime+1, t):
                                through12.append([i, prevstate])
                            through12.append([t, statenum])                            
                    except (ValueError, IndexError):
                        continue

            det10=list(map(list, zip(*det10)))
            det12=list(map(list, zip(*det12)))
            left10=list(map(list, zip(*left10)))
            through10=list(map(list, zip(*through10)))
            left12=list(map(list, zip(*left12)))
            through12=list(map(list, zip(*through12)))
            left, right=int(entryTime+.5), preemptTime+int(f[4]=='Final-solution')
            increment=1.0/(right-left)
            increment1=cutoff/(right-left)
            output=increment
            output1=increment1

            for T in range(left, right):
                T1=T-entryTime
                data=[simNum, T1, projectDist(trajdist, trajtime, T1)]
                j=bisect(det10[0], T)
                for k in range(j-160, j):
                    data.append(det10[1][k])
                j=bisect(det12[0], T)
                for k in range(j-160, j):
                    data.append(det12[1][k]) 
                j=bisect(left10[0], T)
                for k in range(j-160, j):
                    data.append(left10[1][k]) 
                j=bisect(through10[0], T)
                for k in range(j-160, j):
                    data.append(through10[1][k])  
                j=bisect(left12[0], T)
                for k in range(j-160, j):
                    data.append(left12[1][k]) 
                j=bisect(through12[0], T)
                for k in range(j-160, j):
                    data.append(through12[1][k]) 

                posEx=(2**output- 1)
                diff=output-posEx
                
                if f[4]=='Final-solution':

                    data.extend([output, output+diff, posEx])
                else:
                    data.extend([output1, cutoff*(output+diff), cutoff*posEx])
                output+=increment
                output1+=increment1                            

                Data.append(data)

    with open(f'2022-08-06_Preempt-Input-Matrix_continuous_{cutoff}.csv', "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(Data)

    with open(f'2022-08-06_Preempt-Input-Matrix_raw-matrix_continuous_{cutoff}.csv', "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows([x[1:] for x in Data][1:])
