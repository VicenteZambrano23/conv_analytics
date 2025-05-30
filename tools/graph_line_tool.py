import sqlite3
from pydantic import BaseModel, Field, config
from typing import Annotated, Literal
from utils.summary_func import summary_query
from config.config import db_path
from utils.update_counter import update_counter, get_counter
from utils.update_graph_data import update_graph_data


class GraphLineInput(BaseModel):
    query: Annotated[str, Field(description="Query in SQLite")]
    title: Annotated[str, Field(description="Title for the graph")]
    y_axis_title: Annotated[str, Field(description="Title for the y-axis")]
    x_axis_title: Annotated[str, Field(description="Title for the x-axis")]


def graph_line_tool(input: Annotated[GraphLineInput, "Input to the graph line tool."]):

    query = input.query

    if query.find("SELECT") == -1:
        return "Not SELECT statement"

    counter = get_counter()

    title = input.title
    y_axis_title = input.y_axis_title
    x_axis_title = input.x_axis_title

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(query)
    query_result = cursor.fetchall()
    query_summary = summary_query(str(query_result))

    category_element = [item[0] for item in query_result]
    num_element = [item[1] for item in query_result]

    update_counter()
    count = get_counter()
    graph_data = {
        str(count): {
            "type": "line",
            "query": query,
            "title": title,
            "x_axis_title": x_axis_title,
            "y_axis_title": y_axis_title,
            "x_axis": category_element,
            "y_axis": num_element,
            "filter_added": False,
        }
    }

    update_graph_data(graph_data)
    return f"Line graph correctly added. Title: {title}. Y-axis title: {y_axis_title}.X-axis title: {x_axis_title} Data:{query_summary}"
