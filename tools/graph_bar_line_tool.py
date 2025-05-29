import sqlite3
from pydantic import BaseModel, Field
from typing import Annotated, Literal
from utils.summary_func import summary_query
from config.config import db_path
from utils.update_counter import update_counter, get_counter
from utils.update_graph import update_graph
from utils.update_graph_data import update_graph_data


class GraphBarLineInput(BaseModel):
    query: Annotated[str, Field(description="Query in SQLite")]
    title: Annotated[str, Field(description="Title for the graph")]
    y_bar_axis_title: Annotated[str, Field(description="Title for the y1-axis")]
    y_line_axis_title: Annotated[str, Field(description="Title for the y2-axis")]


def graph_bar_line_tool(
    input: Annotated[GraphBarLineInput, "Input to the graph bar line tool."],
):

    query = input.query
    if query.find("SELECT") == -1:
        return "Not SELECT statement"

    counter = get_counter()
    title = input.title
    y_bar_axis_title = input.y_bar_axis_title
    y_line_axis_title = input.y_line_axis_title

    if query.find("LIMIT") == -1:
        query = query.replace(";", " ")

        query += " LIMIT 10;"
    else:
        query = query

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(query)
    query_result = cursor.fetchall()

    query_summary = summary_query(str(query_result))
    category_element = [item[0] for item in query_result]
    num_element_bar = [item[1] for item in query_result]
    num_element_line = [item[2] for item in query_result]

    update_counter()
    graph_data = {
        str(counter + 1): {
            "type": "bar_line",
            "query": query,
            "title": title,
            "y_bar_axis_title": y_bar_axis_title,
            "y_line_axis_title": y_line_axis_title,
            "category_element": category_element,
            "num_element_bar": num_element_bar,
            "num_element_line": num_element_line,
            "filter_added": False,
        }
    }

    update_graph_data(graph_data)
    return f"Bar-LIne graph correctly added. Title: {title}. Y-bar-axis title: {y_bar_axis_title}. Y-line-axis title: {y_bar_axis_title} Data:{query_summary}"
