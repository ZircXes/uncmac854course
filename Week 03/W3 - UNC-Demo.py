# -*- coding: utf-8 -*-
"""
Created on Thu May 28 07:12:14 2020

@author: Chris Kennedy
"""

import pandas as pd
import numpy as np
from sklearn import tree
from graphviz import Source
from sklearn.tree import export_graphviz
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix

# Import
filepath = filepath = r'W3 - UNC Choice Data.xlsx'
df = pd.read_excel(filepath)

# X (Independent) and Y (Dependent)
dfY = df['UNC?']
dfX = df.drop(columns=['Applicant','Choice','UNC?'])

# No dummy variable/categorical variables required (get_dummies)

# Build Decision Tree (no details/limits)
clf = tree.DecisionTreeClassifier(random_state=42)
clf = clf.fit(dfX, dfY)

# Describe tree results
tree.plot_tree(clf)
export_graphviz(clf, out_file="outfile.dot", feature_names= dfX.columns)
Source.from_file("outfile.dot")

# Build Logistic Regression
# Note that Sci-Kit Learn regularizes by default. I use penalty='none' to get the 
# result without regularization to compare with EXCEL if you like
log_reg = LogisticRegression(solver="lbfgs",  penalty='none', random_state=42)
log_reg.fit(dfX,dfY)

# Prepare coefficients for a nice dictionary
keys = []
keys.append("Intercept")
for item in dfX.columns:
    keys.append(item)
    
log_reg_coefficients = np.concatenate((np.array(log_reg.intercept_), np.array(log_reg.coef_[0])))
log_reg_model_desc = dict(zip(keys,log_reg_coefficients.T))

# Output dictionary results in a nice table
print("  Model:")
print("%20s" % "Coefficient", "  %9s" % "Value")
print("%20s" % "--------------------", "  %9s" % "---------")
for key in log_reg_model_desc:
    print('%20s' % key, ': %9.4f' % log_reg_model_desc[key])

# Create Predictions and Confusion Matrix
yPred = pd.DataFrame(log_reg.predict(dfX), columns=['YPred'])
ComparisonDF = pd.DataFrame(data=np.column_stack((dfY.values, yPred.values[:,0])), columns=['Actual','Predicted'])
confusion_matrix(dfY, yPred)

###########################
# Regularized Logistic Regression
log_reg = LogisticRegression(solver="lbfgs", random_state=42)
log_reg.fit(dfX,dfY)

# Prepare coefficients for a nice dictionary
keys = []
keys.append("Intercept")
for item in dfX.columns:
    keys.append(item)
    
log_reg_coefficients = np.concatenate((np.array(log_reg.intercept_), np.array(log_reg.coef_[0])))
log_reg_model_desc = dict(zip(keys,log_reg_coefficients.T))

# Output dictionary results in a nice table
print("  Model (Regularized:")
print("%20s" % "Coefficient", "  %9s" % "Value")
print("%20s" % "--------------------", "  %9s" % "---------")
for key in log_reg_model_desc:
    print('%20s' % key, ': %9.4f' % log_reg_model_desc[key])
    
# Create Predictions & Confusion Matrix
yPred = pd.DataFrame(log_reg.predict(dfX), columns=['YPred'])
ComparisonDF = pd.DataFrame(data=np.column_stack((dfY.values, yPred.values[:,0])), columns=['Actual','Predicted'])
confusion_matrix(dfY, yPred)