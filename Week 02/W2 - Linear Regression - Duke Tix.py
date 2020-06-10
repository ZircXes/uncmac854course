# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 10:54:19 2020

@author: Chris
"""

import os
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge
from sklearn import metrics
import datetime

# Import (Would change to your directory)
# #EDIT# You may need to use workingDir if your Python doesn't look to 
# #EDIT#   the local run folder for this python file.
# #EDIT#   if you need this, adjust the workingDir and uncomment os.chdir()
workingDir = 'OneDrive\\Documents\\Recordings\\Week 02'
# os.chdir(workingDir)
dfDuke = pd.read_excel(r'W2 - DukeTixA.xlsx')

# Data Cleaning
#1 Prepare Row Numbers
dfDuke['Row (Clean)'] = dfDuke['Row'].str.strip()
dfDuke['Row Number'] = dfDuke['Row (Clean)'].apply( lambda x: \
      ord(x)-96 if len(x) == 1 else ord(x[0])-96)
df = dfDuke.drop(columns=['Observation','Row','Row (Clean)'])

#2 Deal with Dates
game_day = dfDuke['Date'].max()
df['Days to Game'] = (game_day - df['Date']) / datetime.timedelta(days=1)
df = df.drop(columns=['Date'])

# Deal with Deck
df['Upper Deck'] = pd.get_dummies(df['Deck'], drop_first=True)
df = df.drop(columns=['Deck'])

# Deal with UNC and Duke Ranks
df['RankSum'] = df['UNC rank'] + df['Duke rank']
df['RankDif'] = abs(df['UNC rank'] - df['Duke rank'])
df = df.drop(columns=['UNC rank','Duke rank'])

# Convert Quantity to One-Hot Encoding
dfQ = pd.get_dummies(df['Quantity'], drop_first=True,prefix='Quantity')
df = df.join(dfQ)
df = df.drop(columns=['Quantity'])

# Make interaction term with lower deck and row number
df['Row +* Lower Deck'] = (1 - df['Upper Deck']) * df['Row Number']

# Convert to X and Y
Y = df['Price']
X = df.drop(columns=['Price'])

# Fit Model
simple = LinearRegression().fit(X, Y)
clf = Ridge(alpha = 1.0)
regularized = clf.fit(X, Y)

# Make Predictions on original X
Yp = simple.predict(X)
Ypr = regularized.predict(X)

# Get R2-Score & Standard error
print("Summary Stats:")
print("%8s" % "METHOD", "%9s" % "R2", "%9s" % "STDERR")
print("%8s" % "OLS", "%9.4f" % metrics.r2_score(Y, Yp), "%9.4f" % (metrics.mean_squared_error(Y, Yp) ** 0.5))
print("%8s" % "RIDGE", "%9.4f" % metrics.r2_score(Y, Ypr), "%9.4f" % (metrics.mean_squared_error(Y, Ypr) ** 0.5))
print("")

#  Simple vs. Regularized (Ridge)
cols= len(X.columns)
coeffs = [simple.coef_, regularized.coef_]
print("Coefficients:")
print ("%16s" % "VAR", "%12s" % "OLS", "%12s" % "RIDGE")
print ("%16s" % "CONSTANT", "%12.4f" % simple.intercept_, "%12.4f" % regularized.intercept_)    
for i in range(0,cols):
    print("%16s" % X.columns[i], "%12.4f" % coeffs[0][i], "%12.4f" % coeffs[1][i])
