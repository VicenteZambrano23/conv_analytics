import sqlite3
from pydantic import BaseModel, Field
from typing import Annotated, Literal
from utils.summary_func import summary_query
from config.config import db_path
from utils.update_counter import update_counter, get_counter
from utils.get_graph_data import get_graph_data
from utils.update_json_fields import update_json_fields


class FilterInput(BaseModel):
    graphic_number: Annotated[
        int, Field(description="Position when the graphic is generated")
    ]


def add_filter_tool(
    input: Annotated[FilterInput, "Input to the graph bar filter tool."],
):

    counter = input.graphic_number
    data = get_graph_data(counter)

    try:
        if data is None:
            raise ValueError("Input 'data' cannot be None.")

        chart_type = data.get("type")  # Using .get() for safer access
        title = data.get("title")

        if chart_type is None:
            raise KeyError("Missing 'type' key in data.")

        # Update JSON field - this assumes update_json_fields handles potential errors or expects counter as int
        update_json_fields(str(counter), "filter_added", True)

        if chart_type == "bar":
            y_axis_title = data.get("y_axis_title")
            if y_axis_title is None:
                raise KeyError("Missing 'y_axis_title' for bar chart.")
            return (
                f"Filter in Bar Graph correctly added. Numeric filter in {y_axis_title}"
            )

        elif chart_type == "scatter":
            y_axis_title = data.get("y_axis")
            x_axis_title = data.get("x_axis")
            if y_axis_title is None or x_axis_title is None:
                raise KeyError("Missing 'y_axis' or 'x_axis' for scatter chart.")
            return f"Filter in Scatter Graph correctly added. Numeric filter in {y_axis_title} and in {x_axis_title}"

        elif chart_type == "line":
            x_axis_title = data.get("x_axis_title")
            if x_axis_title is None:
                raise KeyError("Missing 'x_axis_title' for line chart.")
            return f"Filter in Line Graph correctly added. Date filter in {x_axis_title}"  # Corrected "Scatter Graph" to "Line Graph"

        elif chart_type == "bar_line":
            x_axis_title = data.get("category_element")
            if x_axis_title is None:
                raise KeyError("Missing 'category_element' for bar_line chart.")
            return f"Filter in Bar-Line Graph correctly added. Date filter in {x_axis_title}"  # Corrected "Scatter Graph" to "Bar-Line Graph"

        elif chart_type == "pie":
            return "No filters available for Pie Chart"

        else:
            return f"Unknown chart type: {chart_type}. No filter information available."

    except ValueError as ve:
        # Handle cases where 'data' is None
        return f"Error: Invalid input data. {ve}"
    except KeyError as ke:
        # Handle cases where expected keys are missing
        return f"Error: Missing data. {ke}"
    except Exception as e:
        # Catch any other unexpected errors
        return f"An unexpected error occurred: {e}"
