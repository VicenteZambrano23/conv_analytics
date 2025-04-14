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

class MyConversableAgent(autogen.ConversableAgent):
    async def a_get_human_input(self, prompt: str,print_queue,user_queue) -> str:
        input_prompt = "Please input your further direction, or type 'approved' to proceed, or type 'exit' to end the conversation"

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