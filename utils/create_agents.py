from autogen import ConversableAgent, UserProxyAgent
from config.config import AZURE_OPENAI_CONFIG
from utils.read_prompt import read_text_file
import os
import autogen
prompt_path = os.path.join(os.path.dirname(__file__), '..', 'prompts')

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

    from utils.front_class import MyConversableAgent

def create_userproxy():
    user_proxy = MyConversableAgent(
        name="User_Proxy",
        code_execution_config=False,
        is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
        human_input_mode="ALWAYS",
    )
    user_proxy.register_reply(
        [autogen.Agent, None],
        reply_func=print_messages, 
        config={"callback": None},
    )

    executor_query = ConversableAgent(
        name="executor_query",
        system_message=read_text_file(os.path.join(prompt_path, 'executor_query_prompt.txt')),
        llm_config=AZURE_OPENAI_CONFIG,
         description=read_text_file(os.path.join(prompt_path, 'executor_query_desc.txt')),
    )

    executor_query.register_reply(
            [autogen.Agent, None],
            reply_func=print_messages, 
            config={"callback": None},
        )

    sql_proxy = ConversableAgent(
        name="sql_proxy",
        system_message=read_text_file(os.path.join(prompt_path, 'sql_proxy_prompt.txt')),
        llm_config=AZURE_OPENAI_CONFIG,
         description=read_text_file(os.path.join(prompt_path, 'sql_proxy_desc.txt')),
    )

    sql_proxy.register_reply(
            [autogen.Agent, None],
            reply_func=print_messages, 
            config={"callback": None},
        )


    query_agent = ConversableAgent(
        name="query_agent",
        system_message=read_text_file(os.path.join(prompt_path, 'query_agent_prompt.txt')),
        llm_config=AZURE_OPENAI_CONFIG,
         description=read_text_file(os.path.join(prompt_path, 'query_agent_desc.txt')),
    )

    query_agent.register_reply(
            [autogen.Agent, None],
            reply_func=print_messages, 
            config={"callback": None},
        )

    eval_query_agent = ConversableAgent(
        name="eval_query_agent",
        system_message=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/query_agent_prompt.txt'),
        llm_config=AZURE_OPENAI_CONFIG,
         description=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/query_agent_desc.txt'),
    )

    graph_agent = ConversableAgent(
        name="graph_agent",
        system_message=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/graph_agent_prompt.txt'),
        llm_config=AZURE_OPENAI_CONFIG,
         description=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/graph_agent_desc.txt'),
    )

    graph_eval_agent = ConversableAgent(
        name="graph_eval_agent",
        system_message=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/graph_eval_agent_prompt.txt'),
        llm_config=AZURE_OPENAI_CONFIG,
         description=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/graph_eval_agent_desc.txt'),
    )

    graph_executor = ConversableAgent(
        name="graph_executor",
        system_message=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/executor_graph_agent.txt'),
        llm_config=AZURE_OPENAI_CONFIG,
         description=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/executor_graph_desc.txt'),
    )



    return user_proxy,sql_proxy,query_agent,executor_query,eval_query_agent, graph_agent, graph_eval_agent, graph_executor

  