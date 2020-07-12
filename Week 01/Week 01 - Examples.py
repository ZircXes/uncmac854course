#!/usr/bin/env python
# coding: utf-8

# # Week 01 Example Statistics in Python 3
# This Notebook introduces basic statistical analysis from week 01 using Python 3.x.
# 
# Jupyter notebooks blend Markdown (rich formatted text) with software code and output to ease the learning process.
# 

# Version: 01
# 
# Author: Chris Kennedy

# In[1]:


import pandas as pd
from scipy import stats


# In[2]:


dfWine = pd.read_excel(r'W1 - Wine Quality.xlsx')


# In[3]:


dfWine.describe()


# ## Practice Question 1
# What is the 99% confidence interval for the average alcohol level of a bottle of wine?

# In[4]:


n = dfWine['alcohol'].count()
print("# Wines: %6.2f" % n)


# In[5]:


avg = dfWine['alcohol'].mean()
print("Average Alcohol: %6.4f" % avg)


# In[6]:


stderr = dfWine['alcohol'].sem()
print("Standard Error: %6.4f" % stderr)


# In[7]:


t_CI = stats.t.ppf(0.995,df = n - 1)
print("T-statistic: %6.4f" % t_CI)


# In[8]:


moe = t_CI * stderr
print("Margin of error: %6.4f" % moe)


# In[9]:


print("Lower: %6.4f" % (avg - moe))
print("Upper: %6.4f" % (avg + moe))


# In[10]:


# Concise using stats package directly:
stats.t.interval(0.99, loc=avg, scale=stderr, df = n-1)


# ## Practice Question 2
# What is the 90% confidence interval around the proportion of white wines that are rated very good quality (7 or higher)?
# 

# In[11]:


filteredDF = dfWine[dfWine['type'] == 'white']
n = filteredDF['type'].count()


# In[12]:


qfilteredDF = filteredDF[filteredDF['quality'] >= 7]
nq = qfilteredDF['type'].count()


# In[13]:


proportion  = nq / n
print("Proportion: %5.2f%%" % (proportion*100))


# In[14]:


stderr = (proportion * (1 - proportion) / n)**0.50
print("Standard error: %5.2f%%" % (stderr*100))


# In[15]:


z_CI = stats.norm.ppf(0.95)


# In[16]:


print ("Z for 90%%: %6.4f" % z_CI)


# In[17]:


stats.norm.interval(0.90, loc=proportion*100, scale=stderr*100)


# ## Question 3
# Can you conclude (at the 5% significance level) that the average fixed acid level for all wines is above 7.2?

# In[18]:


def getStatistic(x, H0, stderr):
    return (x - H0) / stderr


# H$_0$: $\mu \le 7.2$
# 
# H$_a$: $\mu > 7.2$
# 

# In[19]:


H0 = 7.20
avg = dfWine['fixed acidity'].mean()
stderr = dfWine['fixed acidity'].sem()
tStatistic = getStatistic(avg, H0, stderr)
nWines = dfWine['fixed acidity'].count()
print("T-stat: %7.4f" %tStatistic)
dfWine['fixed acidity'].describe()


# Right tail test due to alternative hypothesis.

# In[20]:


prob_value = 1 - stats.t.cdf(tStatistic, df=nWines-1)
print(prob_value)


# In[21]:


stats.norm.interval(0.9, loc=5,scale=2
                )


# ### End of Notebook!
