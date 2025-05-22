

import sqlite3


connection = sqlite3.connect(
    "/teamspace/studios/this_studio/conv_analytics/database/mydatabase.db"
)
cursor = connection.cursor()
print("Database connection successful!")

# Execute a simple query
cursor.execute(
    """
UPDATE Orders 
SET OrderDate = DATE(OrderDate, '+28 years', '+2 months');
"""
)
connection.commit()

# Optional: Close the connection when done
cursor.close()
connection.close()

connection = sqlite3.connect(
    "/teamspace/studios/this_studio/conv_analytics/database/mydatabase.db"
)
cursor = connection.cursor()
print("Database connection successful!")
cursor.execute(
    """
SELECT * FROM Orders
"""
)
tables = cursor.fetchall()

print(tables)