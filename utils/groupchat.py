from autogen import GroupChat, GroupChatManager,ConversableAgent,UserProxyAgent
from autogen.agentchat import agent
from config.config import AZURE_OPENAI_CONFIG
from utils.create_agents import read_text_file,create_agents
from autogen import register_function
from tools.get_sql_tables_tool import get_sql_tables_tool
from utils.register_func import register_functions

def create_group_chat():

    agents = create_agents()
    
    def state_transition(last_speaker,group_chat):
        if last_speaker is agents[2]:
            # init -> retrieve
            return agents[0]
        elif last_speaker is agents[0]:
            # retrieve: action 1 -> action 2
            return agents[1]
        elif last_speaker is agents[1]:
         
            return agents[3]
        elif last_speaker is agents[3]:
            return agents[2]

            
    register_functions(agents)

    group_chat = GroupChat(
        agents=[agents[0],agents[1],agents[2],agents[3]],
        messages=[],
        speaker_selection_method=state_transition,
        max_round=100,
       
    )


    group_chat_manager = GroupChatManager(
        groupchat=group_chat,
        llm_config=AZURE_OPENAI_CONFIG,
    )
    agents[2].initiate_chat(
        group_chat_manager,
        message="I need the tables from the database",
    )

