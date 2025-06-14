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
from tools.graph_bar_line_tool import graph_bar_line_tool
from tools.retrieve_tool import retrieve_tool
from tools.internet_tool import internet_tool
from utils.update_counter import reset_counter
from utils.update_graph import update_graph
from utils.clean_graph import graph_clean
from utils.clean_graph_data import clean_graph_data
from tools.add_filter_tool import add_filter_tool
import json
from tools.acronym_tool import acronym_tool
clean_graph_data()
get_sql_tables()
reset_counter()

json_path  = os.path.join(os.path.dirname(__file__), 'database/graph_data.json')

app = Flask(__name__)
cors = CORS(app)

chat_status = "ended"

# Queues for single-user setup
print_queue = queue.Queue()
user_queue = queue.Queue()


class MyConversableAgent(autogen.ConversableAgent):
    async def a_get_human_input(self, prompt: str) -> str:
        input_prompt = "Hello!"

        print_queue.put({"user": "System", "message": input_prompt})

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
    print(
        f"Messages from: {sender.name} sent to: {recipient.name} | num messages: {len(messages)} | message: {messages[-1]}"
    )

    content = messages[-1]["content"]

    if all(key in messages[-1] for key in ["name"]):
        print_queue.put({"user": messages[-1]["name"], "message": content})
    elif messages[-1]["role"] == "user":
        print_queue.put({"user": sender.name, "message": content})
    else:
        print_queue.put({"user": recipient.name, "message": content})

    return False, None  # conversation continued


async def initiate_chat(agent, recipient, message):
    result = await agent.a_initiate_chat(
        recipient, message=message, clear_history=False
    )
    print(result)

    return result


def run_chat(request_json):
    global chat_status
    manager = None
    assistants = []
    try:
        # a) Data structure for the request
        user_input = request_json.get("message")

        # b) UserProxy creation
        userproxy = create_userproxy()
        # c) Chat creation
        manager, assistants = create_groupchat(userproxy)
        # d) Chat start
        asyncio.run(initiate_chat(userproxy, manager, user_input))

        chat_status = "ended"

    except Exception as e:
        chat_status = "error"
        print_queue.put({"user": "System", "message": f"An error occurred: {str(e)}"})


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
        system_message=read_text_file(
            "/teamspace/studios/this_studio/conv_analytics/prompts/executor_query_prompt.txt"
        ),
        llm_config=AZURE_OPENAI_CONFIG,
        description=read_text_file(
            "/teamspace/studios/this_studio/conv_analytics/prompts/executor_query_desc.txt"
        ),
    )
    executor_query.register_reply(
        [autogen.Agent, None],
        reply_func=print_messages,
        config={"callback": None},
    )

    assistants.append(executor_query)

    sql_proxy = ConversableAgent(
        name="sql_proxy",
        system_message=read_text_file(
            "/teamspace/studios/this_studio/conv_analytics/prompts/sql_proxy_prompt.txt"
        ),
        llm_config=AZURE_OPENAI_CONFIG,
        description=read_text_file(
            "/teamspace/studios/this_studio/conv_analytics/prompts/sql_proxy_desc.txt"
        ),
    )

    sql_proxy.register_reply(
        [autogen.Agent, None],
        reply_func=print_messages,
        config={"callback": None},
    )

    assistants.append(sql_proxy)

    query_agent = ConversableAgent(
        name="query_agent",
        system_message=read_text_file(
            "/teamspace/studios/this_studio/conv_analytics/prompts/query_agent_prompt.txt"
        ),
        llm_config=AZURE_OPENAI_CONFIG,
        description=read_text_file(
            "/teamspace/studios/this_studio/conv_analytics/prompts/query_agent_desc.txt"
        ),
    )

    query_agent.register_reply(
        [autogen.Agent, None],
        reply_func=print_messages,
        config={"callback": None},
    )

    assistants.append(query_agent)

    graph_agent = ConversableAgent(
        name="graph_agent",
        system_message=read_text_file(
            "/teamspace/studios/this_studio/conv_analytics/prompts/graph_agent_prompt.txt"
        ),
        llm_config=AZURE_OPENAI_CONFIG,
        description=read_text_file(
            "/teamspace/studios/this_studio/conv_analytics/prompts/graph_agent_desc.txt"
        ),
    )
    graph_agent.register_reply(
        [autogen.Agent, None],
        reply_func=print_messages,
        config={"callback": None},
    )

    assistants.append(graph_agent)

    graph_executor = ConversableAgent(
        name="graph_executor",
        system_message=read_text_file(
            "/teamspace/studios/this_studio/conv_analytics/prompts/executor_graph_agent.txt"
        ),
        llm_config=AZURE_OPENAI_CONFIG,
        description=read_text_file(
            "/teamspace/studios/this_studio/conv_analytics/prompts/executor_graph_desc.txt"
        ),
    )
    graph_executor.register_reply(
        [autogen.Agent, None],
        reply_func=print_messages,
        config={"callback": None},
    )

    assistants.append(graph_executor)

    add_filter_agent = ConversableAgent(
        name="add_filter_agent",
        system_message=read_text_file(
            "/teamspace/studios/this_studio/conv_analytics/prompts/add_filter_agent_prompt.txt"
        ),
        llm_config=AZURE_OPENAI_CONFIG,
        description=read_text_file(
            "/teamspace/studios/this_studio/conv_analytics/prompts/add_filter_agent_desc.txt"
        ),
    )
    add_filter_agent.register_reply(
         [autogen.Agent, None],
        reply_func=print_messages,
        config={"callback": None},
    )
    assistants.append(add_filter_agent)
    
    RAG_agent = ConversableAgent(
        name="RAG_agent",
        system_message=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/RAG_agent_prompt.txt'),
        llm_config=AZURE_OPENAI_CONFIG,
         description=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/RAG_agent_desc.txt'),
    )

    RAG_agent.register_reply(
        [autogen.Agent, None],
        reply_func=print_messages,
        config={"callback": None},
    )
    assistants.append(RAG_agent)

    terminology_agent = ConversableAgent(
        name="terminology_agent",
        system_message=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/terminology_agent_prompt.txt'),
        llm_config=AZURE_OPENAI_CONFIG,
         description=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/terminology_agent_desc.txt'),
    )

    terminology_agent.register_reply(
        [autogen.Agent, None],
        reply_func=print_messages,
        config={"callback": None},
    )
    assistants.append(terminology_agent)



    add_filter_executor = ConversableAgent(
        name="add_filter_executor",
        system_message=read_text_file(
            "/teamspace/studios/this_studio/conv_analytics/prompts/add_filter_executor_prompt.txt"
        ),
        llm_config=AZURE_OPENAI_CONFIG,
        description=read_text_file(
            "/teamspace/studios/this_studio/conv_analytics/prompts/add_filter_executor_desc.txt"
        ),
    )
    add_filter_executor.register_reply(
        [autogen.Agent, None],
        reply_func=print_messages,
        config={"callback": None},
    )
    assistants.append(add_filter_executor)

    RAG_executor = ConversableAgent(
        name="RAG_executor",
        system_message=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/executor_RAG_agent.txt'),
        llm_config=AZURE_OPENAI_CONFIG,
         description=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/executor_RAG_desc.txt'),
    )

    RAG_executor.register_reply(
        [autogen.Agent, None],
        reply_func=print_messages,
        config={"callback": None},
    )

    assistants.append(RAG_executor)

    terminology_executor = ConversableAgent(
        name="terminology_executor",
        system_message=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/executor_terminology_agent.txt'),
        llm_config=AZURE_OPENAI_CONFIG,
         description=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/executor_terminology_desc.txt'),
    )

    terminology_executor.register_reply(
        [autogen.Agent, None],
        reply_func=print_messages,
        config={"callback": None},
    )


    assistants.append(terminology_executor)

    internet_agent = ConversableAgent(
        name="internet_agent",
        system_message=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/internet_agent_prompt.txt'),
        llm_config=AZURE_OPENAI_CONFIG,
         description=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/internet_agent_desc.txt'),
    )

    internet_agent.register_reply(
        [autogen.Agent, None],
        reply_func=print_messages,
        config={"callback": None},
    )
    assistants.append(internet_agent)

    internet_executor = ConversableAgent(
        name="internet_executor",
        system_message=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/executor_internet_agent.txt'),
        llm_config=AZURE_OPENAI_CONFIG,
         description=read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/executor_internet_desc.txt'),
    )

    internet_executor.register_reply(
        [autogen.Agent, None],
        reply_func=print_messages,
        config={"callback": None},
    )

    assistants.append(internet_executor)

    register_function(
        query_tool,
        caller=query_agent,
        executor=executor_query,
        name="query_tool",
        description=str(
            read_text_file(
                "/teamspace/studios/this_studio/conv_analytics/prompts/query_tool_desc.txt"
            )
        ),
    )
    register_function(
        graph_bar_tool,
        caller=graph_agent,
        executor=graph_executor,
        name="graph_bar_tool",
        description=str(
            read_text_file(
                "/teamspace/studios/this_studio/conv_analytics/prompts/graph_bar_tool_desc.txt"
            )
        ),
    )
    register_function(
        graph_line_tool,
        caller=graph_agent,
        executor=graph_executor,
        name="graph_line_tool",
        description=str(
            read_text_file(
                "/teamspace/studios/this_studio/conv_analytics/prompts/graph_line_tool_desc.txt"
            )
        ),
    )
    register_function(
        graph_pie_tool,
        caller=graph_agent,
        executor=graph_executor,
        name="graph_pie_tool",
        description=str(
            read_text_file(
                "/teamspace/studios/this_studio/conv_analytics/prompts/graph_pie_tool_desc.txt"
            )
        ),
    )

    register_function(
        graph_scatter_tool,
        caller=graph_agent,
        executor=graph_executor,
        name="graph_scatter_tool",
        description=str(
            read_text_file(
                "/teamspace/studios/this_studio/conv_analytics/prompts/graph_scatter_tool_desc.txt"
            )
        ),
    )
    register_function(
        graph_bar_line_tool,
        caller=graph_agent,
        executor=graph_executor,
        name="graph_bar_line_tool",
        description=str(read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/graph_bar_line_tool_desc.txt')),
    )

    register_function(
        add_filter_tool,
        caller=add_filter_agent,
        executor=add_filter_executor,
        name="add_filter_tool",
        description=str(
            read_text_file(
                "/teamspace/studios/this_studio/conv_analytics/prompts/add_filter_tool_desc.txt"
            )
        ),
    )

    register_function(
        retrieve_tool,
        caller=RAG_agent,
        executor=RAG_executor,
        name="retrieve_tool",
        description=str(read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/retrieve_tool_desc.txt')),
    )

    register_function(
        acronym_tool,
        caller=terminology_agent,
        executor=terminology_executor,
        name="acronym_tool",
        description=str(read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/acronym_tool_desc.txt')),
    )

    register_function(
        internet_tool,
        caller=internet_agent,
        executor=internet_executor,
        name="internet_tool",
        description=str(read_text_file('/teamspace/studios/this_studio/conv_analytics/prompts/internet_tool_desc.txt')),
    )


    def state_transition(last_speaker, group_chat):

        if last_speaker is sql_proxy:
            return user_proxy

        elif last_speaker is executor_query:
            return sql_proxy

        elif last_speaker is graph_executor:
            return sql_proxy

        elif last_speaker is RAG_executor:
            return sql_proxy
        
        elif last_speaker is internet_executor:
            return sql_proxy

        elif last_speaker is query_agent:
            return executor_query

        elif last_speaker is graph_agent:
            return graph_executor
        
        elif last_speaker is add_filter_agent:
            return add_filter_executor

        elif last_speaker is add_filter_executor:
            return sql_proxy

        elif last_speaker is RAG_agent:
            return RAG_executor
        
        elif last_speaker is terminology_agent:
            return terminology_executor
        
        elif last_speaker is internet_agent
            return internet_executor
        else:
            return "auto"

    if len(assistants) == 1:
        manager = assistants[0]

    elif len(assistants) > 1:
        groupchat = autogen.GroupChat(
            agents=[user_proxy] + assistants,
            messages=[],
            max_round=100,
            speaker_selection_method=state_transition,
            allowed_or_disallowed_speaker_transitions={
                executor_query: [user_proxy],
                query_agent: [user_proxy],
                graph_agent: [user_proxy],
                add_filter_agent: [user_proxy],
                terminology_agent:[user_proxy],
            },
            speaker_transitions_type="disallowed",
        )
        manager = autogen.GroupChatManager(
            groupchat=groupchat,
            llm_config=AZURE_OPENAI_CONFIG,
            system_message="",
        )

    return manager, assistants


@app.route("/api/start_chat", methods=["POST", "OPTIONS"])
def start_chat():
    if request.method == "OPTIONS":
        return jsonify({}), 200
    elif request.method == "POST":
        global chat_status
        try:

            if chat_status == "error":
                chat_status = "ended"

            with print_queue.mutex:
                print_queue.queue.clear()
            with user_queue.mutex:
                user_queue.queue.clear()

            chat_status = "Chat ongoing"

            thread = threading.Thread(target=run_chat, args=(request.json,))
            thread.start()

            return jsonify({"status": chat_status})
        except Exception as e:
            return jsonify({"status": "Error occurred", "error": str(e)})


@app.route("/api/send_message", methods=["POST"])
def send_message():
    user_input = request.json["message"]
    user_queue.put(user_input)
    return jsonify({"status": "Message Received"})


@app.route("/api/get_message", methods=["GET"])
def get_messages():
    global chat_status

    if not print_queue.empty():
        msg = print_queue.get()
        return jsonify({"message": msg, "chat_status": chat_status}), 200
    else:
        return jsonify({"message": None, "chat_status": chat_status}), 200

@app.route('/api/data', methods=['GET'])
def get_json_data():
    """
    API endpoint to retrieve the entire content of a JSON file.

    Reads the specified JSON file and returns its content as a JSON response.
    Handles cases where the file is not found or cannot be parsed.
    """
    if not os.path.exists(json_path):
        # Return a 404 error if the file does not exist
        return jsonify({"error": f"JSON file '{json_path}' not found."}), 404

    try:
        with open(json_path, 'r') as f:
            # Load the JSON content from the file
            data = f.read()
            json_data = json.loads(data)
            return jsonify(json_data), 200
    except json.JSONDecodeError:
        # Return a 500 error if the file content is not valid JSON
        return jsonify({"error": f"Error decoding JSON from '{json_path}'. File might be malformed."}), 500
    except Exception as e:
        # Catch any other unexpected errors
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5009, debug=True)
