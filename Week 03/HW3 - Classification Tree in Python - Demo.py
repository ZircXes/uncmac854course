# -*- coding: utf-8 -*-
"""
Created on Thu May 28 07:12:14 2020

@author: Chris
"""

import pandas as pd
from sklearn import tree
from graphviz import Source
from sklearn.tree import export_graphviz
import os

# Import
filepath = filepath = r'Mushroom.xlsx'
df = pd.read_excel(filepath)

# X (Independent) and Y (Dependent)
dfY = df['Edible']
dfX = df.drop(columns=['Edible'])

# Assign dummy variables
dfYCat = pd.get_dummies(dfY, drop_first=True)
dfXCat = pd.get_dummies(dfX, drop_first=True)

# Build Decision Tree (no details/limits)
clf = tree.DecisionTreeClassifier(max_depth=5, random_state=42)
clf = clf.fit(dfXCat, dfYCat)

# Describe tree results
tree.plot_tree(clf)
export_graphviz(clf, out_file="outfile.dot", feature_names= dfXCat.columns)
Source.from_file("outfile.dot")