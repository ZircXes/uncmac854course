# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 10:41:21 2020
Use SQLITE3 with Python to run queries with SQL (or Python Dataframes) 
This is an alternative to MS Access for those interested in programming or SQL

# Demo for week 4 material in Python with SQLITE3

@author: Chris
"""

import sqlite3
import pandas as pd

# Fancier connection function with error trapping
def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except sqlite3.Error as e:
        print(f"The error '{e}' occured")
        
    return connection

# Connect to a database
# #EDIT# You will need to specify where you want the database stored.
connection = create_connection("C:\\SQLite3\sm_app.sqlite")

# Read in Data Frames
# #NOTE# Make sure you specify your working directory to the same folder as PY
dfBase = pd.read_excel(r'W4 - Wholesale Customer Data.xlsx')
dfTax = pd.read_excel(r'W4 - Regional Tax Rates Data.xlsx')

# TODO: Need to add a primary key for customers when importing these
 
# Create tables in Database (Thanks Pandas!)
dfBase.to_sql('WholesaleData', connection, if_exists='append', index=False)
dfTax.to_sql('TaxRates', connection, if_exists='replace',index=False)

# Execute queries on the database
# Q1
# In which regions are total expenditures by restaurants on frozen items
#   greater than those for deli items?

# Pure Dataframe approach (Python/Pandas)
filterA = dfBase['Channel'] == 'Restaurant'
groupA = dfBase[filterA].groupby(['Region']).sum()
filterB = groupA['Frozen'] > groupA['Deli']
resultQ1 = groupA[filterB]
print(result[['Frozen','Deli']])

# SQL-Dataframe Hybrid Approach
query_q1a = """
SELECT Region, sum(Frozen), sum(Deli)
FROM WholesaleData
WHERE Channel = 'Restaurant'
GROUP BY Region;
"""
tmpResult = pd.read_sql_query(query_q1a, connection)
resultQ1 = tmpResult[tmpResult['sum(Frozen)'] > tmpResult['sum(Deli)']]

# Full SQL Approach: Uses a two-level SQL query; normally broken out into two
#  when doing this in MS Access
query_q1full = """
SELECT Region, SumFrozen, SumDeli
FROM
 (SELECT Region, sum(Frozen) as SumFrozen, sum(Deli) as SumDeli
  from WholesaleData
  where Channel = 'Restaurant'
  GROUP BY Region)
WHERE SumFrozen > SumDeli;
"""
resultQ1 = pd.read_sql_query(query_q1full, connection)

# Q3
# Provide a rank-ordered list of the top 20 Retail customers
#   based on total sales
# TODO: Add customer id once I add primary key
query_q3full = """
SELECT Channel, (Fresh + Dairy + Grocery + Frozen + Cleaning + Deli) as TotalSales 
FROM WholesaleData
WHERE Channel = 'Retail'
ORDER BY TotalSales Desc
LIMIT 20;
"""
resultQ3 = pd.read_sql_query(query_q3full, connection)

# Q4
# Create Query that shows total sales to each customer both Pre&Post-Tax
# Using a conditional join (slower)
query_q4full = """
SELECT A.Channel, A.Region, 
      (A.Fresh + A.Dairy + A.Grocery + A.Frozen + A.Cleaning + A.Deli) as TotalPreTaxSales, 
      B.TaxRate,
      ((A.Fresh + A.Dairy + A.Grocery + A.Frozen + A.Cleaning + A.Deli) * (1 - B.TaxRate)) as TotalPostTaxSales
FROM WholesaleData as A, TaxRates as B
WHERE A.Region = B.Region
ORDER BY TotalPostTaxSales DESC;
"""
resultQ4 = pd.read_sql_query(query_q4full, connection)

# Write result to an Excel file for review
# #EDIT# you can write any of the results to file
resultQ4.to_excel(r'W4 - Q4 Demo.xlsx')

# END