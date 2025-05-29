import sqlite3
from pydantic import BaseModel, Field
from typing import Annotated, Literal
from config.config import db_path
from utils.summary_func import summary_query


class QueryInput(BaseModel):
    query: Annotated[str, Field(description="Query in SQLite")]


def query_tool(input: Annotated[QueryInput, "Input to the query tool."]):
    """
    Executes a SQL query against the Chinook SQLite database.

    This function takes a SQL query as input, connects to the Chinook database,
    executes the query, and returns the result. It handles potential SQLite errors
    and ensures the database connection is closed properly.

    Args:
        input (QueryInput): A NamedTuple containing the SQL query to execute.

    Returns:
        list: A list of tuples representing the query result. Each tuple corresponds
              to a row in the result set. Returns None if an error occurs.
    """
    try:
        query = input.query

        if query.find("SELECT") == -1:
            return "Not SELECT statement"

        # Connect to the database (or create it if it doesn't exist)
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        print("Database connection successful!")

        # Execute a simple query
        cursor.execute(query)

        query_result = cursor.fetchall()
        print(query_result)
        query_summary = summary_query(str(query_result))

        return query_summary
    except sqlite3.Error as error:
        print(f"Error occurred: {error}")

    finally:
        if connection:
            connection.close()
        print("SQLite connection closed.")
