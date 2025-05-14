import pandas as pd
import mysql.connector
import os

# Load the dataset
df = pd.read_csv('books_dataset.csv')

# Normalize column names to lowercase
df.columns = df.columns.str.lower()

# Ensure required columns are present
required_columns = ['isbn', 'title', 'author', 'genre', 'publisher', 'publicationyear', 'pagecount']
if not all(column in df.columns for column in required_columns):
    raise ValueError(f"CSV file is missing one or more required columns: {required_columns}")

# Railway connection settings
connection = mysql.connector.connect(
    host='trolley.proxy.rlwy.net',
    port=35708,
    user='root',
    password='',  # Use real Railway password. This is safe for a local script — don’t commit to GitHub
    database='railway'
)

cursor = connection.cursor()

# Insert data into the database
for _, row in df.iterrows():
    cursor.execute(
        """
        INSERT IGNORE INTO Books (isbn, title, author, genre, publisher, publication_year, page_count)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (row['isbn'], row['title'], row['author'], row['genre'], row['publisher'], row['publicationyear'], row['pagecount'])
    )

# Commit changes and close connection
connection.commit()
cursor.close()
connection.close()

print("Books dataset loaded to Railway DB successfully!")
