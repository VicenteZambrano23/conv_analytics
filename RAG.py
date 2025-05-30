import autogen
import os
from autogen import AssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
from config.config import AZURE_OPENAI_CONFIG
from chromadb.utils import embedding_functions
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"), model_name="text-embedding-ada-002"
)

recur_spliter = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=200,
    separators=["\n", "\r", "\t", "\n\n", ". ", " ", ""],
)

assistant = AssistantAgent(
    name="assistant",
    system_message="You are a helpful assistant.",
    llm_config=AZURE_OPENAI_CONFIG,
)

docs_path = os.path.join(
    os.path.dirname(__file__), "..", "database/RAG_files/Acronyms.pdf"
)
ragproxyagent = RetrieveUserProxyAgent(
    name="ragproxyagent",
    retrieve_config={
        "task": "qa",
        "docs_path": docs_path,
        "get_or_create": True,  # set to False if you don't want to reuse an existing collection
        "overwrite": False,  # set to True if you want to overwrite an existing collection
        "custom_text_split_function": recur_spliter.split_text,
        # "client": chromadb.PersistentClient().get_or_create_collection(name = 'autogen_agent', embedding_function=openai_ef)
    },
)
assistant.reset()
_context = {"problem": "What is ANZ?"}
ret_msg = ragproxyagent.message_generator(ragproxyagent, None, _context)
print(ret_msg)
# ragproxyagent.initiate_chat(assistant,message=ragproxyagent.message_generator, problem="What are electic fuel cell hybrid vehicles?")
