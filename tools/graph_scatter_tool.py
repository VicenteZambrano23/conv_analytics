import sqlite3
from pydantic import BaseModel, Field
from typing import Annotated, Literal
from utils.summary_func import summary_query
from config.config import db_path
from utils.update_counter import update_counter, get_counter
from utils.update_graph import update_graph
from utils.update_graph_data import update_graph_data


class GraphScatterInput(BaseModel):
    query: Annotated[str, Field(description="Query in SQLite")]
    title: Annotated[str, Field(description="Title for the graph")]
    x_axis: Annotated[str, Field(description="X-Axis name for the graph")]
    y_axis: Annotated[str, Field(description="Y-Axis name for the graph")]


def graph_scatter_tool(
    input: Annotated[GraphScatterInput, "Input to the graph scatter tool."],
):
    query = input.query
    if query.find("SELECT") == -1:
        return "Not SELECT statement"

    counter = get_counter()

    title = input.title
    x_axis = input.x_axis
    y_axis = input.y_axis

    if "LIMIT" not in query.upper():  # Using .upper() for case-insensitive check
        query = query.replace(";", " ")
        query += " LIMIT 10;"
    else:
        query = query  # No change if LIMIT is already present

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(query)

    rows = cursor.fetchall()
    query_summary = summary_query(str(rows))

    chart_series_data = []  # Initialize an empty list to store series data

    if len(rows[0]) == 3:
        for row in rows:
            category = row[0]
            value_1 = row[1]
            value_2 = row[2]
            chart_series_data.append({"name": category, "data": [[value_1, value_2]]})
    else:
        # If there are only two columns, treat them as a single series
        # You might want to refine the 'name' here based on context if possible
        single_series_data = []
        for row in rows:
            value_1 = row[0]
            value_2 = row[1]
            single_series_data.append([value_1, value_2])
        chart_series_data.append({"name": "Data Points", "data": single_series_data})

    update_counter()

    graph_data = {
        str(counter + 1): {
            "type": "scatter",
            "query": query,
            "title": title,
            "x_axis": x_axis,
            "y_axis": y_axis,
            "data": chart_series_data,  # Directly assign the list of dictionaries
            "filter_added": "No",  # Update this logic if you have filter detection
        }
    }
    update_graph_data(graph_data)

    return f"Scatter graph correctly added. Title: {title}. Y-axis title: {y_axis}. X-axis: {x_axis} Data:{query_summary}"
