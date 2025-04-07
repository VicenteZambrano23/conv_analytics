from autogen import register_function
from tools.get_sql_tables_tool import get_sql_tables_tool
from tools.query_tool import query_tool
from utils.create_agents import create_agents
from utils.read_prompt import read_text_file



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
        get_sql_tables_tool,
        caller=agents[0],
        executor=agents[1],
        name="get_sql_tables_tool",
        description=str(read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/get_sql_tables_descriptions.txt')),
    )

    register_function(
        query_tool,
        caller=agents[4],
        executor=agents[5],
        name="query_tool",
        description=str(read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/query_tool_desc.txt')),
    )
