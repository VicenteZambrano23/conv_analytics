import sqlite3

try:
# Connect to the database (or create it if it doesn't exist)
    connection = sqlite3.connect('/teamspace/studios/this_studio/conv_analytics/database/chinook.db')
    cursor = connection.cursor()
    print("Database connection successful!")

    # Execute a simple query
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    result = cursor.fetchall()
    print(f"Query results: {result}")

except sqlite3.Error as error:
    print(f"Error occurred: {error}")

finally:
    if connection:
        connection.close()
    print("SQLite connection closed.")