import autogen
from utils.print_messages import print_messages
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
    return user_proxy