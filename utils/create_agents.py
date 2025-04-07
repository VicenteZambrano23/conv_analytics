from autogen import ConversableAgent, UserProxyAgent
from config.config import AZURE_OPENAI_CONFIG
from utils.read_prompt import read_text_file


def create_agents():
    """
    Creates and initializes multiple ConversableAgent instances for a SQL querying workflow.

    This function sets up several agents with specific roles and configurations
    to facilitate interactions with a SQL database. Each agent is configured with
    a system message, LLM configuration, human input mode, and a description,
    all loaded from text files.

    The agents created are:
    - get_sql_tables_agent: Retrieves the schema of SQL tables.
    - user_proxy: Acts as a proxy for user input.
    - executor_database_schema: Interprets the schema to help build queries.
    - executor_query: Executes the sql query.
    - sql_proxy: acts as a middle man to execute sql.
    - query_agent: Formulates SQL queries based on user requests.

    Returns:
        tuple: A tuple containing the initialized agent instances in the order:
               (get_sql_tables_agent, executor_database_schema, user_proxy, sql_proxy, query_agent, executor_query).
    """

    get_sql_tables_agent = ConversableAgent(
        name="get_sql_tables_agent",
        system_message=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/get_sql_tables_prompt.txt'),
        llm_config=AZURE_OPENAI_CONFIG,
        human_input_mode="NEVER",
        description=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/get_sql_tables_desc.txt'),
    )


    user_proxy = UserProxyAgent(
        name="user_proxy",
        human_input_mode="ALWAYS",
        description=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/user_proxy_desc.txt'),
    )

    executor_database_schema = ConversableAgent(
        name="executor_database_schema",
        system_message=read_text_file('//teamspace/studios/this_studio/conv_analytics/prompts/executer_database_schema_prompt.txt'),
        llm_config=AZURE_OPENAI_CONFIG,
         description=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/executor_database_schema_desc.txt'),
    )

    executor_query = ConversableAgent(
        name="executor_query",
        system_message=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/executor_query_prompt.txt'),
        llm_config=AZURE_OPENAI_CONFIG,
         description=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/executor_query_desc.txt'),
    )

    sql_proxy = ConversableAgent(
        name="sql_proxy",
        system_message=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/sql_proxy_prompt.txt'),
        llm_config=AZURE_OPENAI_CONFIG,
         description=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/sql_proxy_desc.txt'),
    )

    query_agent = ConversableAgent(
        name="query_agent",
        system_message=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/query_agent_prompt.txt'),
        llm_config=AZURE_OPENAI_CONFIG,
         description=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/query_agent_desc.txt'),
    )

    return get_sql_tables_agent,executor_database_schema,user_proxy,sql_proxy,query_agent,executor_query

  