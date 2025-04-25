import os
import time
import asyncio
import threading
import autogen
from flask import Flask, request, jsonify
from flask_cors import CORS
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent
from autogen.agentchat import AssistantAgent, UserProxyAgent
import queue
from autogen import ConversableAgent
from utils.read_prompt import read_text_file
from config.config import AZURE_OPENAI_CONFIG
from autogen import register_function
from tools.query_tool import query_tool
from tools.graph_bar_tool import graph_bar_tool
from utils.clean_graph import graph_clean
from utils.get_sql_tables import get_sql_tables
from tools.graph_line_tool import graph_line_tool
from tools.graph_pie_tool import graph_pie_tool
from tools.graph_scatter_tool import graph_scatter_tool
from utils.update_counter import reset_counter
from utils.update_graph import update_graph

get_sql_tables()
reset_counter()
update_graph()

app = Flask(__name__)
cors=CORS(app)

chat_status = "ended"  

# Queues for single-user setup
print_queue = queue.Queue()
user_queue = queue.Queue()


class MyConversableAgent(autogen.ConversableAgent):
    async def a_get_human_input(self, prompt: str) -> str:
        input_prompt = "Hello!"

        print_queue.put({'user': "System", 'message': input_prompt})

        start_time = time.time()
        global chat_status
        chat_status = "inputting"
        while True:
            if not user_queue.empty():
                input_value = user_queue.get()
                chat_status = "Chat ongoing"
                print("input message: ", input_value)
                return input_value

            if time.time() - start_time > 600:  
                chat_status = "ended"
                return "exit"

            await asyncio.sleep(1) 

def print_messages(recipient, messages, sender, config):
    print(f"Messages from: {sender.name} sent to: {recipient.name} | num messages: {len(messages)} | message: {messages[-1]}")

    content = messages[-1]['content']

    if all(key in messages[-1] for key in ['name']):
        print_queue.put({'user': messages[-1]['name'], 'message': content})
    elif messages[-1]['role'] == 'user':
        print_queue.put({'user': sender.name, 'message': content})
    else:
        print_queue.put({'user': recipient.name, 'message': content})

    return False, None #conversation continued  
         
async def initiate_chat(agent, recipient, message):
    result = await agent.a_initiate_chat(recipient, message=message, clear_history=False)
    print(result)

    return result
def run_chat(request_json):
    global chat_status
    manager = None
    assistants = []
    try:
        # a) Data structure for the request
        user_input = request_json.get('message')
        
        # b) UserProxy creation
        userproxy = create_userproxy()
        # c) Chat creation
        manager, assistants = create_groupchat(userproxy) 
        # d) Chat start
        asyncio.run(initiate_chat(userproxy, manager, user_input))

        chat_status = "ended"

    except Exception as e:
        chat_status = "error"
        print_queue.put({'user': "System", 'message': f"An error occurred: {str(e)}"})

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


def create_groupchat(user_proxy):  
     
    assistants = []

    executor_query = ConversableAgent(
        name="executor_query",
        system_message=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/executor_query_prompt.txt'),
        llm_config=AZURE_OPENAI_CONFIG,
         description=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/executor_query_desc.txt'),
    )
    executor_query.register_reply(
            [autogen.Agent, None],
            reply_func=print_messages, 
            config={"callback": None},
        ) 

    assistants.append(executor_query)

    sql_proxy = ConversableAgent(
        name="sql_proxy",
        system_message=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/sql_proxy_prompt.txt'),
        llm_config=AZURE_OPENAI_CONFIG,
         description=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/sql_proxy_desc.txt'),
    )

    sql_proxy.register_reply(
            [autogen.Agent, None],
            reply_func=print_messages, 
            config={"callback": None},
        ) 

    assistants.append(sql_proxy)

    query_agent = ConversableAgent(
        name="query_agent",
        system_message=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/query_agent_prompt.txt'),
        llm_config=AZURE_OPENAI_CONFIG,
         description=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/query_agent_desc.txt'),
    )

    query_agent.register_reply(
            [autogen.Agent, None],
            reply_func=print_messages, 
            config={"callback": None},
        ) 

    assistants.append(query_agent)

    eval_query_agent = ConversableAgent(
        name="eval_query_agent",
        system_message=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/query_agent_prompt.txt'),
        llm_config=AZURE_OPENAI_CONFIG,
         description=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/query_agent_desc.txt'),
    )

    eval_query_agent.register_reply(
            [autogen.Agent, None],
            reply_func=print_messages, 
            config={"callback": None},
        ) 

    assistants.append(eval_query_agent)
    graph_agent = ConversableAgent(
        name="graph_agent",
        system_message=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/graph_agent_prompt.txt'),
        llm_config=AZURE_OPENAI_CONFIG,
         description=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/graph_agent_desc.txt'),
    )
    graph_agent.register_reply(
            [autogen.Agent, None],
            reply_func=print_messages, 
            config={"callback": None},
        ) 

    assistants.append(graph_agent)

    graph_eval_agent = ConversableAgent(
        name="graph_eval_agent",
        system_message=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/graph_eval_agent_prompt.txt'),
        llm_config=AZURE_OPENAI_CONFIG,
         description=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/graph_eval_agent_desc.txt'),
    )
    graph_eval_agent.register_reply(
            [autogen.Agent, None],
            reply_func=print_messages, 
            config={"callback": None},
        ) 

    assistants.append(graph_eval_agent)

    graph_executor = ConversableAgent(
        name="graph_executor",
        system_message=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/executor_graph_agent.txt'),
        llm_config=AZURE_OPENAI_CONFIG,
         description=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/executor_graph_desc.txt'),
    )
    graph_executor.register_reply(
            [autogen.Agent, None],
            reply_func=print_messages, 
            config={"callback": None},
        ) 

    assistants.append(graph_executor)
    register_function(
        query_tool,
        caller=eval_query_agent,
        executor=executor_query,
        name="query_tool",
        description=str(read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/query_tool_desc.txt')),
    )
    register_function(
        graph_bar_tool,
        caller=graph_eval_agent,
        executor=graph_executor,
        name="graph_bar_tool",
        description=str(read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/graph_bar_tool_desc.txt')),
    )
    register_function(
        graph_line_tool,
        caller=graph_eval_agent,
        executor=graph_executor,
        name="graph_line_tool",
        description=str(read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/graph_line_tool_desc.txt')),
    )
    register_function(
        graph_pie_tool,
        caller=graph_eval_agent,
        executor=graph_executor,
        name="graph_pie_tool",
        description=str(read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/graph_pie_tool_desc.txt')),
    )

    register_function(
        graph_scatter_tool,
        caller=graph_eval_agent,
        executor=graph_executor,
        name="graph_scatter_tool",
        description=str(read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/graph_scatter_tool_desc.txt')),
    )

    def state_transition(last_speaker,group_chat):

        if last_speaker is query_agent:
            return eval_query_agent

        elif last_speaker is sql_proxy:
            return user_proxy

        elif last_speaker is graph_agent:
            return graph_eval_agent

        elif last_speaker is graph_executor:
            return sql_proxy
        else:
            return 'auto'
    if len(assistants) == 1: 
        manager = assistants[0]

    elif len(assistants) > 1: 
        groupchat = autogen.GroupChat(
            agents=[user_proxy] + assistants, 
            messages=[], 
            max_round=100,
            speaker_selection_method=state_transition,
            allowed_or_disallowed_speaker_transitions = {
            eval_query_agent : [user_proxy],
            executor_query : [user_proxy],
            graph_executor : [user_proxy],
            query_agent : [user_proxy],
            graph_eval_agent : [user_proxy],
            graph_agent : [user_proxy],
        },
        speaker_transitions_type="disallowed",
        )
        manager = autogen.GroupChatManager(
            groupchat=groupchat, 
            llm_config=AZURE_OPENAI_CONFIG, 
            system_message="",
        )

    return manager, assistants

@app.route('/api/start_chat', methods=['POST', 'OPTIONS']) 
def start_chat():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    elif request.method == 'POST':
        global chat_status
        try:

            if chat_status == 'error':
                chat_status = 'ended' 

            with print_queue.mutex:
                print_queue.queue.clear()
            with user_queue.mutex:
                user_queue.queue.clear()

            chat_status = 'Chat ongoing'

            thread = threading.Thread(
                target=run_chat, 
                args=(request.json,)
            )
            thread.start()
    
            return jsonify({'status': chat_status})
        except Exception as e:
            return jsonify({'status': 'Error occurred', 'error': str(e)})
        
@app.route('/api/send_message', methods=['POST'])
def send_message():
    user_input = request.json['message']
    user_queue.put(user_input)
    return jsonify({'status': 'Message Received'})

@app.route('/api/get_message', methods=['GET'])
def get_messages():
    global chat_status 

    if not print_queue.empty():
        msg = print_queue.get()  
        return jsonify({'message': msg, 'chat_status': chat_status}), 200
    else:
        return jsonify({'message': None, 'chat_status': chat_status}), 200
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5008, debug=True)