from autogen import ConversableAgent, UserProxyAgent
from config.config import AZURE_OPENAI_CONFIG
from utils.read_prompt import read_text_file


def create_agents():

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

    intermediate_agent = ConversableAgent(
        name="intermediate_agent",
        system_message=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/get_sql_tables_prompt.txt'),
        llm_config=AZURE_OPENAI_CONFIG,
         description=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/intermediate_agent_desc.txt'),
    )

    sql_proxy = ConversableAgent(
        name="sql_proxy",
        system_message=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/sql_proxy_prompt.txt'),
        llm_config=AZURE_OPENAI_CONFIG,
         description=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/sql_proxy_desc.txt'),
    )

    return get_sql_tables_agent,intermediate_agent,user_proxy,sql_proxy

  