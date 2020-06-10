# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 10:54:19 2020

Data from: https://www.kaggle.com/pavansubhasht/ibm-hr-analytics-attrition-dataset

To look for lines to edit see #EDIT# in comments
For notes see #NOTE# in comments

@author: Chris
"""

# Imports/Libraries/Packages
import os
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import numpy as np

# Import Data

# #EDIT# change this workingDir to make it work to your directory.
workingDir = 'OneDrive\\Documents\\Recordings\\Extra'


os.chdir(workingDir)
df = pd.read_csv(r'A - WA_Fn-UseC_-HR-Employee-Attrition.csv')

# DATA PREPARATION
# #EDIT# To get a list of columns use this line
df.columns

# #EDIT# Add more variables here to XCols, don't mess with YCols
XCols = ['Age','JobLevel']

YCols = ['Attrition']

# Create X and Y dataframes based on our choices.
X = df[XCols]
Y = pd.get_dummies(df[YCols], drop_first=True)

# Clean up categoricals and drop first category - (alphabetical sorted columns)
# #EDIT# Any variaables that you need to convert from categorical text 
# #EDIT# or numbers that need to be one-hot encoded, specify here.
# #EDIT# I included 'Gender' to get you started
XD = pd.get_dummies(df[['Gender']], drop_first=True)

# Adjust X Dataset
X = X.join(XD)
# #EDIT# this column list needs to match the get_dummies list above.
X = X.drop(columns=['Gender'])

# SPLITTING DATA for Validation
# #NOTE# an alternative is cross-validation (better); can look online.
X_train, X_test, y_train, y_test = train_test_split( \
     X, Y, test_size=0.33, random_state=1138)

# Write splits of data to file
X_train.to_csv('X_train.csv')
X_test.to_csv('X_test.csv')
y_train.to_csv('y_train.csv')
y_test.to_csv('y_test.csv')

## Hyperparameter Search for Regularized Logistic Regression:
# Smaller 'c' = stronger Regularization
c_choices = np.logspace(7,-7,num=15, base=2)

# Build the model (Standard Logistic Regression, and Regularized)
log_reg = LogisticRegression(solver="lbfgs",  penalty='none', random_state=1138, max_iter=1000)
log_reg.fit(X_train, y_train)

# Loop through and build logistic regression models
result = []
for index_c in c_choices:
    log_l2_reg = LogisticRegression(solver="lbfgs", C=index_c, penalty='l2', random_state=1138, max_iter=1000)
    log_l2_reg.fit(X_train, y_train)
    yPr = pd.DataFrame(log_l2_reg.predict(X_test), columns=['yPred_Attrition'])
    tn, fp, fn, tp = confusion_matrix(y_test, yPr).ravel()
    # #NOTE# if you get any divide by zero errors, let me know. 
    accuracy = (tp + tn) / (tn + fp + fn + tp)
    recall = tp / (tp + fn)
    precision = tp / (tp + fp)
    result.append(recall)

# Decide on what c you want to use
# #EDIT# Update your final "c" here for regularization
c_choice = 1.0
log_reg = LogisticRegression(solver="lbfgs",  C=c_choice, penalty='none', random_state=1138, max_iter=1000)
log_reg.fit(X_train, y_train)

# Prepare coefficients for a nice dictionary
keys = []
keys.append("Intercept")
for item in X.columns:
    keys.append(item)
    
log_reg_coefficients = np.concatenate((np.array(log_reg.intercept_), np.array(log_reg.coef_[0])))
log_l2_reg_coefficients = np.concatenate((np.array(log_l2_reg.intercept_), np.array(log_l2_reg.coef_[0])))
log_reg_model_desc = dict(zip(keys,log_reg_coefficients.T))
log_l2_reg_model_desc = dict(zip(keys,log_l2_reg_coefficients.T))

# Output dictionary results in a nice table
print("")
print("%24s" % "Coefficient", "  %12s" % "Ordinary", "%12s" % "L2Penalty")
print("%24s" % "--------------------", "  %12s" % " -----------", "%12s" % " -----------")
for key in log_reg_model_desc:
    print('%24s' % key, ': %12.4f' % log_reg_model_desc[key], '%12.4f' % log_l2_reg_model_desc[key])
    
# END
    
