import sqlite3
from pydantic import BaseModel, Field
from typing import Annotated, Literal
from utils.summary_func import summary_query
from config.config import db_path
from utils.update_counter import update_counter, get_counter
from utils.update_graph_data import update_graph_data


class GraphPieInput(BaseModel):
    query: Annotated[str, Field(description="Query in SQLite")]
    title: Annotated[str, Field(description="Title for the graph")]


def graph_pie_tool(input: Annotated[GraphPieInput, "Input to the graph pie tool."]):

    query = input.query

    if query.find("SELECT") == -1:
        return "Not SELECT statement"

    counter = get_counter()

    title = input.title

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(query)
    query_result = cursor.fetchall()
    query_summary = summary_query(str(query_result))

    category_element = [item[0] for item in query_result]
    num_element = [item[1] for item in query_result]

    update_counter()

    graph_data = {
        str(counter + 1): {
            "type": "pie",
            "query": query,
            "title": title,
            "category": category_element,
            "nums": num_element,
            "filter_added": "No",
        }
    }
    update_graph_data(graph_data)
    return f"Pie graph correctly added. Title: {title}. Data:{query_summary}"
