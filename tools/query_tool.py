import sqlite3
from pydantic import BaseModel, Field
from typing import Annotated, Literal

class QueryInput(BaseModel):
    query: Annotated[str, Field(description="Query in SQLite")]

def query_tool(input: Annotated[QueryInput, "Input to the query tool."]):
    try:
        query = input.query
# Connect to the database (or create it if it doesn't exist)
        connection = sqlite3.connect('/teamspace/studios/this_studio/conv_analytics/database/chinook.db')
        cursor = connection.cursor()
        print("Database connection successful!")

        # Execute a simple query
        cursor.execute(query)
        query_result = cursor.fetchall()
        
        return query_result
    except sqlite3.Error as error:
        print(f"Error occurred: {error}")

    finally:
        if connection:
            connection.close()
        print("SQLite connection closed.")
