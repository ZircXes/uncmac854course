# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 15:55:33 2020

@author: Chris
"""

import matplotlib.pyplot as plt
import numpy as np

tpr = [0.5,0.5,0.6,0.6,0.8,0.8,0.9,0.9,1.0,1.0]
fpr = [0.0,0.1,0.1,0.2,0.2,0.5,0.5,0.8,0.8,1.0]

plt.figure()

# Dotted line for 100%
plt.plot([0,1],[1,1], color='black', linestyle='--', lw=1)

# 0-> 1 line for 50/50 (no predictive power)
plt.plot([0,1],[0,1], color='navy', linestyle='--', lw=2)

# ROC plot
plt.plot(fpr, tpr, color='darkorange', label='ROC curve', lw=2)

# set up axes
plt.xlim([0.0,1.0])
plt.ylim([0.0,1.05])

# set up labels
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic (ROC)')
plt.legend(loc="lower right")

plt.show()

## Scatter plot, correlated random variables
x = np.array([0, 5])
y = np.array([-3,7])
means = [x.mean(), y.mean()]  
std = [x.std() / 3, y.std() / 3]
corr = 0.65
cov = [[std[0]**2          , std[0]*std[1]*corr], 
        [std[0]*std[1]*corr,           std[1]**2]] 

result = np.random.multivariate_normal(means, cov, 5000).T
plt.scatter(result[0], result[1], alpha=0.1)