# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 10:54:19 2020

@author: Chris
"""

import os
import pandas as pd
from scipy import stats

# Import (Would change to your directory)
## CHANGE ME CHANGE ME CHANGE ME ##
workingDir = 'OneDrive\\Documents\\Recordings\\Week 01'
## NO NEED TO CHANGE AFTER THIS LINE

os.chdir(workingDir)
dfWine = pd.read_excel(r'W1 - Wine Quality.xlsx')

# Let's start with Wine #################

# Describe your dataset
print("Alcohol, Mean: %6.4f" % dfWine['alcohol'].mean()) # Sample Average
print("Alcohol, Standard Deviation: %6.4f" % dfWine['alcohol'].std()) # Sample Standard Deviation
print("Alcohol, Standard Error: %6.4f" % dfWine['alcohol'].sem()) # Standard Error of the Mean
dfWine.describe()

# Question 1 - Wine
# What is the 99% confidence interval for the average alcohol level 
#  of a bottle of wine?
print ("Wine Q1")

# I could use these as inline functions
# I separate them to make it easier for new programmers
n = dfWine['alcohol'].count()
print ("# Wines: %6.2f" % n)

avg = dfWine['alcohol'].mean()
print("Average Alcohol: %6.4f" % avg)

t_CI = stats.t.ppf(0.995,df = n - 1 )
print ("T-value for 99%% CI: %6.4f" % t_CI)

stderr = dfWine['alcohol'].sem()
print ("Standard error: %6.4f" % stderr)

moe = t_CI * stderr
print ("Margin of Error (MOE): %6.4f" % moe)

print ("Lower: %6.4f" % (avg - moe))
print ("Upper: %6.4f" % (avg + moe))

# or alternatively in a concise formula
stats.t.interval(0.99, loc=avg, scale=stderr, df = n - 1)

# Question 2 - Wine
# What is the 90% confidence interval around the proportion of 
#   white wines that are rated very good quality (7 or higher)? 
print ("Wine Q2")

# Filter on White Wines
filteredDF = dfWine[dfWine['type'] == 'white']
n = filteredDF['type'].count()

# Filter now on Quality >= 7
qfilteredDF = filteredDF[filteredDF['quality'] >= 7]
nq = qfilteredDF['type'].count()

# Get proportion and Standard error
proportion = nq / n
print("Proportion: %5.2f%%" % (proportion*100))

stderr = (proportion * (1 - proportion) / n )**0.50
print("Standard Error: %5.2f%%" % (stderr*100))

z_CI = stats.norm.ppf(0.95)
print ("Z for 90%% CI: %6.4f" % z_CI)

moe = z_CI * stderr
print ("Margin of Error (MOE): %5.2f%%" % (moe*100))

print ("Lower: %5.2f%%" % ((proportion - moe)*100))
print ("Upper: %5.2f%%" % ((proportion + moe)*100))

# or alternatively in a concise formula
stats.norm.interval(0.90, loc=proportion*100, scale=stderr*100)

## Questions 3+ (Wine)
def getStatistic(x, H0, stderr):
    return (x - H0) / stderr

## Question 3
# Can you conclude (at the 5% significance level) that the average fixed acid level for all wines is above 7.2?
H0 = 7.2
avg = dfWine['fixed acidity'].mean()
stderr = dfWine['fixed acidity'].sem()
tStatistic = getStatistic(avg, H0, stderr)
n = dfWine['fixed acidity'].count()
sigLevel = 0.05

# Right tail for Ha (>) 
criticalT = stats.t.ppf(0.95,df=n-1)
probValue = 1 - stats.t.cdf(tStatistic,df=n-1)

# Since probValue not less than Significance Level (alternatively T not > critical T) Cannot reject the null
print("Reject Null") if probValue < sigLevel else print("Cannot Reject Null")


