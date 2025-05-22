from autogen import GroupChat, GroupChatManager
from config.config import AZURE_OPENAI_CONFIG
from utils.create_agents import create_agents
from utils.register_func import register_functions


def create_group_chat():
    """
    Creates and initiates a group chat with multiple agents for a SQL querying workflow.

    This function initializes a group chat involving several agents, each with specific roles,
    to facilitate a conversation aimed at executing SQL queries. It also defines a state
    transition function to control the flow of the conversation between the agents.

    The state transition function `state_transition` determines the next speaker based on
    the last speaker. It defines a specific sequence for the agents to interact.

    The function also registers necessary tools for the agents to use and initiates the
    group chat with a "Hello!" message from the user proxy agent.

    Returns:
        GroupChatManager: An instance of GroupChatManager, which manages the group chat.
    """

    agents = create_agents()

    def state_transition(last_speaker, group_chat):

        if last_speaker is agents[1]:
            return agents[0]

        elif last_speaker is agents[3]:
            return agents[1]
        
        elif last_speaker is agents[5]:
            return agents[1]
        
        elif last_speaker is agents[7]:
            return agents[1]
        
        elif last_speaker is agents[9]:
            return agents[1]

        elif last_speaker is agents[2]:
            return agents[3]

        elif last_speaker is agents[4]:
            return agents[5]

        elif last_speaker is agents [6]:
            return agents[7]
        
        elif last_speaker is agents[8]:
            return agents[9]
        else:
            return "auto"

    register_functions(agents)

    group_chat = GroupChat(
        agents=[agents[0],agents[1],agents[2],agents[3],agents[4],agents[5],agents[6],agents[7],agents[8],agents[9]],
        messages=[],
        speaker_selection_method=state_transition,
        max_round=100,
        allowed_or_disallowed_speaker_transitions = {
            agents[4] : [agents[0]],
            agents[2] : [agents[0]],
            agents[3] : [agents[0]],
            agents[5] : [agents[0]], 
            agents[6] : [agents[0]],
            agents[7] : [agents[0]], 
            agents[8] : [agents[0]],
            agents[9] : [agents[0]]  },
        speaker_transitions_type="disallowed",
    )

    group_chat_manager = GroupChatManager(
        groupchat=group_chat,
        llm_config=AZURE_OPENAI_CONFIG,
    )

    agents[0].initiate_chat(
        group_chat_manager,
        message="Hello!",
    )

    return group_chat_manager, agents
