import pandas as pd
import matplotlib.pyplot as plt
from sklearn import model_selection, preprocessing
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import GridSearchCV
import pickle
import numpy as np 

convertProportion=lambda p: np.log(0.001) if p<=0 else (np.log(1000) if p>=1 else np.log(p / (1 - p)))
class LogitRegression(MLPRegressor):

    def fit(self, x, p):
        p = np.asarray(p)
        y = np.array(list(map(convertProportion, p)))
        return super().fit(x, y)

    def predict(self, x):
        y = super().predict(x)
        return 1.01 / (np.exp(-y) + 1)

x=[]; accu1=[]; accu2=[]; accu=[]

n=0
with open('2022-08-06_Preempt-Input-Matrix_continuous_0.8.csv') as file:
    for line in file:
        n+=1
        features=line.split('\n')[0].split(',')
        if n==1:
            break

features=features[1:]

#features=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','Class']
df=pd.read_csv('2022-08-06_Preempt-Input-Matrix_train_continuous_0.8.csv', header=None, names=features)

for i in range(len(features)):
    if(type(df[features[i]][0])==str):
        le=preprocessing.LabelEncoder()
        le.fit(df[features[i]])
        df[features[i]]=le.transform(df[features[i]])

X = df[features[:-3]]
y = df['Preempt-Decision-Linear']


# for i in range(7, 0,-1):
#     test_size=.125*i
#     print('Cross-validation: test-size=', test_size)
#     X_train_1, X_dummy, Y_train_1, Y_dummy = model_selection.train_test_split(X_train, Y_train, test_size=test_size, random_state=10)
#     parameters = {'alpha': [.01, .001, .0001, 0.00001], 'activation':['logistic']}
#     clf = GridSearchCV(MLPClassifier(solver='adam', max_iter=500),parameters, cv=10, scoring='accuracy')
#     clf.fit(X=X_train_1, y=Y_train_1)
#     clf1 = clf.best_estimator_
#     accu1.append(clf1.score(X_train_1,Y_train_1))
#     accu2.append(clf1.score(X_test,Y_test))
#     x.append(X_train_1.shape[0])
#     clf2=MLPClassifier()
#     clf2=clf2.fit(X=X_train_1, y=Y_train_1)
#     accu.append(clf2.score(X_test,Y_test))  

parameters = {'activation':['logistic', 'identity', 'tanh', 'relu']}
clf = GridSearchCV(LogitRegression(solver='adam', max_iter=1000, learning_rate='adaptive'), parameters, cv=10)
clf.fit(X=X, y=y)
clf = clf.best_estimator_
filename='12NB-NN-EVP-Linear-0.8.model'
clf.fit(X, y)
pickle.dump(clf, open(filename, 'wb'))
