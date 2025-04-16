from autogen import register_function
from tools.query_tool import query_tool
from utils.read_prompt import read_text_file
from tools.graph_tool import graph_tool


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
        caller=agents[4],
        executor=agents[3],
        name="query_tool",
        description=str(read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/query_tool_desc.txt')),
    )
    register_function(
        graph_tool,
        caller=agents[6],
        executor=agents[7],
        name="graph_tool",
        description=str(read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/graph_tool.txt')),
    )

