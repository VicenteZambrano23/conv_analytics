from autogen import register_function
from tools.query_tool import query_tool
from utils.read_prompt import read_text_file
from tools.graph_bar_tool import graph_bar_tool
from tools.graph_line_tool import graph_line_tool
from tools.graph_pie_tool import graph_pie_tool
from tools.graph_scatter_tool import graph_scatter_tool
from tools.graph_bar_line_tool import graph_bar_line_tool
from tools.retrieve_tool import retrieve_tool
from tools.acronym_tool import acronym_tool
from tools.internet_tool import internet_tool
import os

prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts/")


def register_functions(agents):
    """
    Registers functions as tools for specific agents in a multi-agent conversation.

    This function associates the `get_sql_tables_tool` and `query_tool` functions
    with specific agents, making them available as tools for those agents to use.
    It utilizes the `register_function` utility to link the functions with their
    respective caller and executor agents, along with a name and description.

    Args:
        agents (tuple): A tuple containing the initialized agent instances.
                        It expects the agents to be in the order:
                        (get_sql_tables_agent, executor_database_schema, ..., query_agent, executor_query).
    """

    register_function(
        query_tool,
        caller=agents[2],
        executor=agents[3],
        name="query_tool",
        description=str(
            read_text_file(os.path.join(prompt_path, "query_tool_desc.txt"))
        ),
    )

    register_function(
        graph_bar_tool,
        caller=agents[4],
        executor=agents[5],
        name="graph_bar_tool",
        description=str(
            read_text_file(os.path.join(prompt_path, "graph_bar_tool_desc.txt"))
        ),
    )
    register_function(
        graph_line_tool,
        caller=agents[4],
        executor=agents[5],
        name="graph_line_tool",
        description=str(
            read_text_file(os.path.join(prompt_path, "graph_line_tool_desc.txt"))
        ),
    )
    register_function(
        graph_pie_tool,
        caller=agents[4],
        executor=agents[5],
        name="graph_pie_tool",
        description=str(
            read_text_file(os.path.join(prompt_path, "graph_pie_tool_desc.txt"))
        ),
    )

    register_function(
        graph_scatter_tool,
        caller=agents[4],
        executor=agents[5],
        name="graph_scatter_tool",
        description=str(
            read_text_file(os.path.join(prompt_path, "graph_scatter_tool_desc.txt"))
        ),
    )

    register_function(
        graph_bar_line_tool,
        caller=agents[4],
        executor=agents[5],
        name="graph_bar_line_tool",
        description=str(
            read_text_file(os.path.join(prompt_path, "graph_bar_line_tool_desc.txt"))
        ),
    )

    register_function(
        retrieve_tool,
        caller=agents[6],
        executor=agents[7],
        name="retrieve_tool",
        description=str(
            read_text_file(os.path.join(prompt_path, "retrieve_tool_desc.txt"))
        ),
    )

    register_function(
        acronym_tool,
        caller=agents[8],
        executor=agents[9],
        name="acronym_tool",
        description=str(
            read_text_file(os.path.join(prompt_path, "acronym_tool_desc.txt"))
        ),
    )
    register_function(
        internet_tool,
        caller=agents[10],
        executor=agents[11],
        name="internet_tool",
        description=str(
            read_text_file(os.path.join(prompt_path, "internet_tool_desc.txt"))
        ),
    )
