
## Introduction to SQL
Structured Query Language (SQL) is a common data manipulation language that is simple to learn.

While SQL can be used to create, delete, and update tables of data, our focus will be reading, which covers most use cases for non-IT professionals.

SQL consists of only a few keywords which allow you perform a number of extract and transform processes to read and manipulate data.

#### Keywords
* SELECT
* FROM
* WHERE
* GROUP BY
* ORDER BY
* LIMIT

#### Query Form
    SELECT column_name(s)
    FROM table_name(s)
    WHERE criteria
    ORDER BY column_name ASC or DESC

The only required elements are SELECT and FROM, which specify which columns to retrieve from which tables. Given a table of records, the SELECT statement tells us what columns to return, the FROM statement specifies the table(s), and WHERE criteria are filters/conditions.

#### Aggregation Functions
* Sum
* Count
* Avg
* Min / Max


#### Examples

**Table**: Transactions

    RowID     Name       Region      Amount    Date 
    1         Chris      North       20        2020-01-05
    2         Holly      South       5         2020-01-31
    3         Alex       South       7         2020-03-14
    4         Elliott    North       13        2020-04-14
    5         Connor     South       1         2020-05-10
    6         Selena     South       70        2020-06-20

**Select all transactions from the South. Sort by Amount (largest to smallest).**

    SELECT Name, Amount, Region
    FROM Transactions
    WHERE Region = 'South'
    ORDER BY Amount DESC
    
**How many transactions by Regions?**

    SELECT Count(RowID) as NumTransactions, Region
    FROM Transactions
    GROUP BY Region
    
**Select the first 3 records after sorting by Name (alphabetical).**

    SELECT * 
    FROM Transactions
    ORDER BY Name ASC
    LIMIT 3
    
**What is the total amount from transactions in 2020 Q1?**

    SELECT SUM(Amount) as TotalAmountQ1
    FROM Transactions
    WHERE Date BETWEEN '2020-01-01' and '2020-03-31'

**Select records from January that are in the North Region.**

    SELECT RowID, Name, Region, Amount, Date, strftime('%m', Date) as TXMonth
    FROM Transactions
    WHERE Region = 'North' 
      AND TXMonth = '1'
    
**Specify a risk-rating based on Amount (>15 = High, >5 = Medium, otherwise Low). Aggregate number of transactions by risk-rating.

    SELECT count(RowID) as NumTransactions, 
           sum(Amount) as TotalAmount,
           CASE
             WHEN Amount >= 15 THEN '01-High'
             WHEN Amount >= 5 THEN '02-Medium'
             ELSE '03-Low'
           END AS RiskRating
    FROM Transactions
    GROUP BY RiskRating
    
### References
* [EverSQL](https://www.eversql.com/best-and-fastest-way-to-learn-sql/): For-Profit but has a great guide for SQL resources
* [SQL Cheat Sheet](https://www.sqlitetutorial.net/sqlite-cheat-sheet/)

