# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 10:54:19 2020

@author: Chris
"""

import os
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge
from sklearn import metrics
from numpy.linalg import norm
import statsmodels.api as sm

# Import (Would change to your directory)
## CHANGE ME CHANGE ME CHANGE ME ##
workingDir = 'OneDrive\\Documents\\Recordings\\Week 02'
## NO NEED TO CHANGE AFTER THIS LINE
os.chdir(workingDir)
dfBoston = pd.read_excel(r'W2 - Boston Housing.xlsx')

# Describe data
dfBoston.head()

dfBoston.describe()

Y = dfBoston['MEDV']
X = dfBoston.drop(columns=['MEDV'])

# Fit Model
simple = LinearRegression().fit(X, Y)
clf = Ridge(alpha = 1.0)
regularized = clf.fit(X, Y)

# Make Predictions on original X
Yp = simple.predict(X)
Ypr = regularized.predict(X)

# Get R2-Score & Standard error
print(metrics.r2_score(Y, Yp))
print(metrics.mean_squared_error(Y, Yp) ** 0.5)

print(metrics.r2_score(Y, Ypr))
print(metrics.mean_squared_error(Y, Ypr) ** 0.5)

#  Simple vs. Regularized (Ridge)
cols= len(X.columns)
coeffs = [simple.coef_, regularized.coef_]

print ("%8s" % "VAR", "%9s" % "SIMPLE", "%9s" % "RIDGE")
print ("%8s" % "CONSTANT", "%9.4f" % simple.intercept_, "%9.4f" % regularized.intercept_)    
for i in range(0,cols):
    print("%8s" % X.columns[i], "%9.4f" % coeffs[0][i], "%9.4f" % coeffs[1][i])

# Stats Model Comparison
X['const'] = 1
est = sm.OLS(Y, X)
est_model = est.fit()
est_model.summary()