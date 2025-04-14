import asyncio

from jinja2 import utils
from utils.initiate_chat import initiate_chat
from utils.groupchat import create_group_chat
from utils.initiate_chat import initiate_chat

def run_chat(request_json,print_queue):
    global chat_status
    manager = None
    agents = []
    try:
        # a) Data structure for the request
        user_input = request_json.get('message')
        agents_info = request_json.get('agents_info') 
        task_info = request_json.get('task_info')
        # b) UserProxy creation
        # c) Chat creation
        manager, agents = create_group_chat() 
        # d) Chat start
        asyncio.run(initiate_chat(agents[0], manager, user_input))

        chat_status = "ended"

    except Exception as e:
        chat_status = "error"
        print_queue.put({'user': "System", 'message': f"An error occurred: {str(e)}"})
