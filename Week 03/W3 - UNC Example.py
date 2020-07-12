#!/usr/bin/env python
# coding: utf-8

# ## W3 - UNC Example:
# 
# Author: Chris Kennedy

# In[1]:


import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, roc_curve, roc_auc_score, auc
from sklearn import tree
from sklearn.tree import export_graphviz
from graphviz import Source


# ### Data Preparation and Loading

# In[2]:


df = pd.read_excel(r'W3 - UNC Choice Data.xlsx')


# In[3]:


y = df['UNC?']
X = df.drop(columns=['Applicant','Choice','UNC?'])


# In[4]:


X.head()


# ## Logistic Regression

# ### Model Build

# In[5]:


clr = LogisticRegression(solver="lbfgs", penalty='none', random_state=42)
clr.fit(X, y)


# Output coefficients

# In[6]:


print("[Intercept] ", X.columns)
print(clr.intercept_, clr.coef_)


# Prediction and scoring

# In[7]:


yp = clr.predict(X)
y_score = clr.decision_function(X)
print(y_score)


# ### Performance Metrics

# In[8]:


tn, fp, fn, tp = confusion_matrix(y, yp).ravel()


# In[9]:


print("Confusion Matrix:")
print("%32s" % "Predicted")
print("%17s" % " ", "%8s" % "UNC", "%8s" % "Duke")
print("%8s" % "Actual", "%8s" % "UNC", "%8i" % tp, "%8i" % fn)
print("%8s" % " ", "%8s" % "Duke", "%8i" % fp, "%8i" % tn)
print("")
print("Accuracy:    %6.1f%%" % ((tp+tn)/(tp+tn+fp+fn)*100))
print("Sensitivity: %6.1f%%" % (tp/(tp+fn)*100))
print("Specificity: %6.1f%%" % (tn/(tn+fp)*100))


# In[10]:


fpr, tpr, thresholds = roc_curve(y, y_score)
roc_auc = auc(fpr, tpr)


# ### Plots

# In[11]:


import matplotlib.pyplot as plt


# In[12]:


plt.figure()
plt.plot([0, 1],[1,1], color='black', linestyle='--', lw=1)
plt.plot(fpr,tpr, color='darkorange', label='ROC curve (area = %0.2f)' % roc_auc, lw=2)
plt.plot([0, 1],[0,1], color='navy', linestyle='--', lw=2)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic (ROC)')
plt.legend(loc="lower right")
plt.show()


# ## Decision Trees

# In[13]:


dt = tree.DecisionTreeClassifier(random_state = 42, criterion="gini", splitter="best", max_depth=2)
dt = dt.fit(X, y)


# #### Describe the tree

# In[14]:


export_graphviz(dt, out_file="outfile.dot", feature_names=X.columns)
Source.from_file("outfile.dot")


# For each box [a, b] corresponds to counts for [false, true] or [0, 1]

# #### Prediction and Scoring

# In[15]:


ypt = dt.predict(X)
ypt_raw = dt.predict_proba(X)


# #### Performance Metrics

# In[16]:


tnt, fpt, fnt, tpt = confusion_matrix(y, ypt).ravel()


# In[17]:


print("Confusion Matrix:")
print("%32s" % "Predicted")
print("%17s" % " ", "%8s" % "UNC", "%8s" % "Duke")
print("%8s" % "Actual", "%8s" % "UNC", "%8i" % tpt, "%8i" % fnt)
print("%8s" % " ", "%8s" % "Duke", "%8i" % fpt, "%8i" % tnt)
print("")
print("Accuracy:    %6.1f%%" % ((tpt+tnt)/(tpt+tnt+fpt+fnt)*100))
print("Sensitivity: %6.1f%%" % (tpt/(tpt+fnt)*100))
print("Specificity: %6.1f%%" % (tnt/(tnt+fpt)*100))


# In[18]:


fprt, tprt, thresholdst = roc_curve(y, ypt_raw[:,1])
roc_auct = auc(fprt, tprt)


# #### Plots

# In[19]:


plt.figure()
plt.plot([0, 1],[1,1], color='black', linestyle='--', lw=1)
plt.plot(fprt,tprt, color='darkorange', label='ROC curve (area = %0.2f)' % roc_auct, lw=2)
plt.plot([0, 1],[0,1], color='navy', linestyle='--', lw=2)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic (ROC)')
plt.legend(loc="lower right")
plt.show()


# ### End of Notebook!
