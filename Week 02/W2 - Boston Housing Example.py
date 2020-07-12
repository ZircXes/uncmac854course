#!/usr/bin/env python
# coding: utf-8

# ## Week 02 - Boston Housing Example
# 
# This example loads the Boston Housing data example and performs regression in Python. 
# 
# Author: Chris Kennedy
# 

# In[3]:


import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge
from sklearn import metrics


# ### Prepare the Data

# In[5]:


dfBoston = pd.read_excel(r'W2 - Boston Housing.xlsx')


# In[7]:


dfBoston.head(5)


# In[9]:


dfBoston.describe()


# Check for missing/null values

# In[12]:


dfBoston.isnull().sum()


# Check datatypes for regression

# In[14]:


dfBoston.dtypes


# Split the data into X and y:

# In[23]:


y = dfBoston['MEDV']
X = dfBoston.drop(columns=['MEDV'])


# ### Prepare the Regressions

# #### Specify Hyperparameters 
# Normally we would calibrate the regularization parameter using a grid-search or cross-validation; however, for simplicity we are just using $\lambda$ = 10.0.
# 

# In[44]:


regLambda = 10.0 # Note that lambda is a protected word in python


# Given hyperparameters, initialize the models - no hyperparameters for classical linear regression.

# In[45]:


classicLR = LinearRegression()
ridgeLR = Ridge(alpha = regLambda)


# #### Fit the models

# In[24]:


model_CLR = classicLR.fit(X, y)


# In[46]:


model_RLR = ridgeLR.fit(X, y)


# #### Build predictions (in-sample)

# In[47]:


yp = model_CLR.predict(X)
ypr = model_RLR.predict(X)


# #### Simple performance metrics
# We are not using a validation/holdout set this week. Typically cross-validation or train/validate/test splits would apply when evaluating machine learning models.

# In[48]:


print("Classical: ")
print("R2:   %10.3f" % metrics.r2_score(y, yp))
print("RMSE: %10.4f" % metrics.mean_squared_error(y, yp) ** 0.5)
print("")
print("Ridge:")
print("R2:   %10.3f" % metrics.r2_score(y, ypr))
print("RMSE: %10.4f" % metrics.mean_squared_error(y, ypr) ** 0.5)


# #### Output intercepts and coefficients for comparison

# In[49]:


#  Simple vs. Regularized (Ridge)
cols= len(X.columns)
coeffs = [model_CLR.coef_, model_RLR.coef_]

print ("%8s" % "VAR", "%9s" % "SIMPLE", "%9s" % "RIDGE", "%9s" % "Delta")
print ("%8s" % "CONSTANT", "%9.4f" % model_CLR.intercept_, "%9.4f" % model_RLR.intercept_, "%9.4f" % (model_CLR.intercept_ - model_RLR.intercept_))    
for i in range(0,cols):
    print("%8s" % X.columns[i], "%9.4f" % coeffs[0][i], "%9.4f" % coeffs[1][i], "%9.4f" % (coeffs[0][i] - coeffs[1][i]))


# ### Plots and visualizations

# In[50]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rc('axes', labelsize=14)
mpl.rc('xtick', labelsize=12)
mpl.rc('ytick', labelsize=12)


# Plot Y vs. Prediction using Classical and Ridge

# In[64]:


plt.plot(yp, y, "b.", label="Classical")
plt.scatter(ypr, y, s=80, facecolors='none', edgecolors='r', label="Ridge")
plt.xlabel("$y_{predicted}$")
plt.ylabel("$y$")
plt.legend(loc="upper left", fontsize=14)
plt.show()


# Plot residuals for classical and ridge

# In[60]:


plt.plot(y, (yp - y), "b.")
plt.xlabel("$y$")
plt.ylabel("residuals")
plt.show()


# In[63]:


plt.plot(y,(ypr-y), "b.")
plt.show()


# ### End of Notebook!
