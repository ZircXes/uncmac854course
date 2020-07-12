Python with Pandas is a powerful tool for data manipulation. Whether choosing to use Python + Pandas or to use Python + Pandas + SQL, either option is robust for data transformation and manipulation.

We introduced some basic data manipulation with Python and Pandas in Week 01, so this week will focus on using SQL with Python, and additional data-frame concepts.

For this section, we will use the SQLite database (Free) with Python.

### Basic SQLite functionality
#### Imports (Libraries)
```
import pandas as pd
import sqlite3
```

#### Database basics:
Connecting to the database:
Connects to a SQLite database. If the database does not exist, this will create an empty database.
```
connection = sqlite3.connect(path)
```

Loading a table in your database:
This creates a table in the database based on your Pandas dataFrame.
```
dataFrame.to_sql('TableName', connection, if_exists='replace', index=False)
```

Querying your database:
This runs a SQL query and stores the results in a Pandas dataFrame.
```
query = """
SELECT column_name(s)
FROM table_name(s)
WHERE condition(s)
"""
result = pd.read_sql_query(query, connection)
```

### Additional Python Dataframe techniques
Selecting only a set of columns:
```
df[ ['column_a', 'column_b', ..., 'column_n'] ]
```

Group By a column to get a sum or count:
```
df.groupby(['columns']).sum()
df.groupby(['columns']).count()
```

Apply a filter on a dataframe:
```
filter = df['Region'] = 'North'
result = df[filter]
```

Apply a function to a column:
```
result = df['column'].apply(function)
```

Return only the first *n* records:
```
df.head(n)
```

Get the number of records:
```
len(df)
```