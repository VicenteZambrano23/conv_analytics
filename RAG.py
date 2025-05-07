import autogen
from autogen import AssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
from config.config import AZURE_OPENAI_CONFIG
from chromadb.utils import embedding_functions
from langchain.text_splitter import RecursiveCharacterTextSplitter

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                api_key=AZURE_OPENAI_CONFIG,
                model_name="text-embedding-ada-002"
            )

recur_spliter = RecursiveCharacterTextSplitter(separators=["\n", "\r", "\t"])

assistant = AssistantAgent(
    name="assistant",
    system_message="You are a helpful assistant.",
    llm_config=AZURE_OPENAI_CONFIG,
)



ragproxyagent = RetrieveUserProxyAgent(
    name="ragproxyagent",
    retrieve_config={
        "task": "qa",
        "docs_path": "/teamspace/studios/this_studio/conv_analytics/database/RAG_files/Example.md",  
        "get_or_create": True,  # set to False if you don't want to reuse an existing collection
        "overwrite": False,  # set to True if you want to overwrite an existing collection      
       # "custom_text_split_function": recur_spliter.split_text,
       # "embedding_function": openai_ef,
    },
)

assistant.reset()
ragproxyagent.initiate_chat(assistant, message=ragproxyagent.message_generator, problem="What is bluebolt?")

assistant.reset()
userproxyagent = autogen.UserProxyAgent(name="userproxyagent")
userproxyagent.initiate_chat(assistant, message="What is bluebolt?")