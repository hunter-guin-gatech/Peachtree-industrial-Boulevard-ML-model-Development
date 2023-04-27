import pandas as pd
from sklearn import model_selection, preprocessing
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import f1_score
import csv
import pickle
import numpy as np 

cutoff=0.8

convertProportion=lambda p: np.log(0.001) if p<=0 else (np.log(1000) if p>=1 else np.log(p / (1 - p)))
class LogitRegression(MLPRegressor):

    def fit(self, x, p):
        p = np.asarray(p)
        y = np.array(list(map(convertProportion, p)))
        return super().fit(x, y)

    def predict(self, x):
        y = super().predict(x)
        return 1.01 / (np.exp(-y) + 1)

validation_nums=[]
with open('validation_run-num.txt') as file:
    for line in file:
        validation_nums.append(int(line.split('\n')[0]))

n=0
scenario=[]
with open('2022-08-06_Preempt-Input-Matrix_continuous_0.8.csv') as file:
    for line in file:
        n+=1
        f=line.split('\n')[0].split(',')
        if n==1:
            features=f
        else:
            if int(f[0]) in validation_nums:
                scenario.append(f[0])

features=features[1:]

#features=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','Class']
df=pd.read_csv('2022-08-06_Preempt-Input-Matrix_validation_continuous_0.8.csv', header=None, names=features)

for i in range(len(features)):
    if(type(df[features[i]][0])==str):
        le=preprocessing.LabelEncoder()
        le.fit(df[features[i]])
        df[features[i]]=le.transform(df[features[i]])

X_valid = df[features[:-3]]
y_valid = df['Preempt-Decision-NegExp']

filename='12NB-NN-EVP-NegExp-0.8.model'
loaded_model = pickle.load(open(filename, 'rb'))
y_valid_pred = loaded_model.predict(X_valid)


data=[['Scenario', 'y-test', 'y-test-pred', 'False-negatives', 'False-positives', 'P(X==1)']]+[[z, int(x>cutoff), int(y>cutoff), int(x>cutoff and y<=cutoff), int(x<=cutoff and y>cutoff), y] for x, y, z in zip(y_valid, y_valid_pred, scenario)] 

with open(f'2022-08-06_Preempt_12NB_cutoff-{cutoff}_continuous-negExp-validation-output.csv', "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(data)
      