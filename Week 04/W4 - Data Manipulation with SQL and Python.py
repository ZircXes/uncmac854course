#!/usr/bin/env python
# coding: utf-8

# ## Week 04: Data Manipulation and SQL with Python
# 
# Author: Chris Kennedy
# Course: MAC 854 Data Analytics for Accountants

# In[1]:


import pandas as pd
import sqlite3
import re


# Function for connecting to database. Try/Catch functions are useful for databases to understand if the process executed successfully. This is important as some of the activities are external to Python and aren't guaranteed to be captured back through this console.

# In[2]:


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except sqlite3.Error as e:
        print(f"The error '{e}' occured")
        
    return connection


# Helper function to interpret accounting numbers (which could be read in as strings) into numerical data. If a money-type class is available, use that over floating point numbers. Not used in this demo but shown for an example function to illustrate regular expressions and functions that can be used with .apply(f(x))

# In[3]:


def clean_currency(x):
    """ Cleans strings of $ and () to numerical numbers that
    can be converted to a float
    """
    if isinstance(x, str):
        return (re.sub('[(]', '-', re.sub( '[\$,)]', '', x)))
    return (x)


# ### Setup a database locally

# In[4]:


connection = create_connection("localapp.sqlite")


# #### Read in dataframes for analysis

# In[5]:


dfBase = pd.read_excel(r'W4 - Wholesale Customer Data.xlsx')
dfTax = pd.read_excel(r'W4 - Regional Tax Rates Data.xlsx')


# In[6]:


dfBase.head(5)


# In[7]:


dfTax.head(5)


# Add a primary key for the main table

# In[8]:


dfBase['Row'] = dfBase.index + 1


# Load tables into database

# In[9]:


dfBase.to_sql('WholesaleData', connection, if_exists='replace', index=False)
dfTax.to_sql('TaxRates', connection, if_exists='replace', index=False)


# ### Questions
# 1. In which regions are total expenditures by restaurants on frozen items greater than those for deli items?
# 2. Provide a rank-ordered list of the top 20 Retail customers based on total sales.
# 3. Create a query that shows total sales to each customer both before and after tax.
# 
# For each of these questions I'll provide an answer using SQL and with Python data manipulation using Pandas dataframes.

# #### Q1: SQL
# In which regions are total expenditures by restaurants on frozen items greater than those for deli items?

# In[10]:


# Question 1: SQL
query = """
SELECT Region, SumFrozen, SumDeli
FROM
 (SELECT Region, sum(Frozen) as SumFrozen, sum(Deli) as SumDeli
  from WholesaleData
  where Channel = 'Restaurant'
  GROUP BY Region)
WHERE SumFrozen > SumDeli;
"""
result_q1_sql = pd.read_sql_query(query, connection)
print(result_q1_sql)


# #### Q1: Python
# In which regions are total expenditures by restaurants on frozen items greater than those for deli items?
# 
# I break this down into a few steps to make the execution easier to understand:
# 1. Filter on channel = Restaurant
# 2. Aggregate by Region
# 3. Filter on results where Frozen > Deli

# In[11]:


# Question 1: Python
print("Intermediate table:")
filter = dfBase['Channel'] == 'Restaurant'
group_df = dfBase[filter].groupby(['Region']).sum()
print(group_df[['Frozen','Deli']])

print("\nFinal Table:")
filter = group_df['Frozen'] > group_df['Deli']
result_q1_py = group_df[filter]
print(result_q1_py[['Frozen','Deli']])


# #### Q2: SQL
# Provide a rank-ordered list of the top 20 Retail customers based on total sales.
# 

# In[12]:


# Q2: SQL
query = """
SELECT Channel, (Fresh + Dairy + Grocery + Frozen + Cleaning + Deli) as TotalSales 
FROM WholesaleData
WHERE Channel = 'Retail'
ORDER BY TotalSales Desc
LIMIT 20;
"""
result_q2_sql = pd.read_sql_query(query, connection)
print(result_q2_sql)


# #### Q2: Python
# Provide a rank-ordered list of the top 20 Retail customers based on total sales.
# 
# Steps:
# 1. Create the calculated column for Total Sales
# 2. Filter on "Retail"
# 3. Sort by Total Sales, descending
# 4. Select first (top) 20 records
# 

# In[13]:


dfBase['Total Sales'] = dfBase['Fresh'] + dfBase['Dairy'] + dfBase['Grocery'] + dfBase['Frozen'] +                         dfBase['Cleaning'] + dfBase['Deli'] 

filter = dfBase['Channel'] == 'Retail'
result_q2_py = dfBase[filter].sort_values(by=['Total Sales'], ascending=False)

print(result_q2_py[['Channel','Region','Total Sales','Row']].head(20))


# #### Q3: SQL
# Create a query that shows total sales to each customer both before and after tax.

# In[14]:


query = """
SELECT A.Channel, A.Region, 
      (A.Fresh + A.Dairy + A.Grocery + A.Frozen + A.Cleaning + A.Deli) as TotalPreTaxSales, 
      B.TaxRate,
      ((A.Fresh + A.Dairy + A.Grocery + A.Frozen + A.Cleaning + A.Deli) * (1 - B.TaxRate)) as TotalPostTaxSales
FROM WholesaleData as A, TaxRates as B
WHERE A.Region = B.Region
ORDER BY TotalPostTaxSales DESC;
"""
result_q3_sql = pd.read_sql_query(query, connection)
print(result_q3_sql[['Region','Channel','TotalPreTaxSales','TotalPostTaxSales','TaxRate']])


# #### Q3: Python
# Create a query that shows total sales to each customer both before and after tax.
# 
# Steps:
# 1. First merge the tax data into the base dataframe
# 2. Create the calculated column for after tax sales
# 3. Order by Total After Tax Sales

# In[15]:


dfFull = dfBase.merge(dfTax, on='Region')
dfFull['Total After Tax Sales'] = dfFull['Total Sales'] * (1 - dfFull['TaxRate'])
result_q3_py = dfFull.sort_values(by=['Total After Tax Sales'], ascending=False)
print(result_q3_py[['Region','Channel','Total Sales','Total After Tax Sales','TaxRate']])


# ### End of Notebook!
