import sqlite3
from pydantic import BaseModel, Field
from typing import Annotated, Literal
from utils.summary_func import summary_query
from config.config import db_path
from utils.update_counter import update_counter, get_counter
from utils.update_graph import update_graph
from langchain.text_splitter import RecursiveCharacterTextSplitter
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent

docs=["/teamspace/studios/this_studio/conv_analytics/database/RAG_files/Acronyms.pdf"]
recur_spliter = RecursiveCharacterTextSplitter(chunk_size=1500,chunk_overlap=200,separators=["\n", "\r", "\t","\n\n", ". ", " ", ""])
retrieve_agent = RetrieveUserProxyAgent(
        name="retrieve_agent",
        system_message="Assistant who has to search for the meaning of acronyms in the retrieved context",
        human_input_mode="NEVER",
        retrieve_config={
            "task": "qa",
            "docs_path": docs ,  
            "get_or_create": False,  # set to False if you don't want to reuse an existing collection
            "overwrite": True,  # set to True if you want to overwrite an existing collection      
            "custom_text_split_function": recur_spliter.split_text,
            #"client": chromadb.PersistentClient().get_or_create_collection(name = 'autogen_agent', embedding_function=openai_ef)
        },
        code_execution_config=False,  # we don't want to execute code in this case.
    )

class AcronymInput(BaseModel):
    message: Annotated[str,"Acronyms that are present in user questions"]
    n_results: Annotated[int, "number of results"] = 3

def acronym_tool(input: Annotated[AcronymInput, "Input to the acronym tool."] ):

    #rag_agent.n_results = input.n_results  # Set the number of results to be retrieved.
    _context = {"problem": input.message}
    ret_msg = retrieve_agent.message_generator(retrieve_agent, None, _context)
    return ret_msg

