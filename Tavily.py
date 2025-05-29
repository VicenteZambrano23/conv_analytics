import autogen
import os
from autogen import AssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
from config.config import AZURE_OPENAI_CONFIG
from chromadb.utils import embedding_functions
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb
from tavily import TavilyClient
from config.config import TAVILY_API_KEY


#Tavily API to perform the internet Search
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

#response = tavily_client.search("What happened in Spain a few weeks ago?", include_answer=True,) # Perform the internet search

response = tavily_client.search("What happened in Spain a few weeks ago?",include_answer='advanced')#, include_raw_content= True) # Perform the internet search

# Accessing individual pieces of information

print(f"Query: {response['query']}\n")
print(f"Answer: {response['answer']}\n")

# Accessing search results
print("Search Results:")
for i, result in enumerate(response['results']):
    print(f"--- Result {i+1} ---")
    print(f"Title: {result['title']}")
    print(f"URL: {result['url']}")
    print(f"Content Snippet: {result['content'][:200]}...") # Print first 200 chars for brevity
    print(f"Score: {result['score']}")
    #print(f"Raw Content: {result['raw_content']}\n") # Will be None in this example

print(f"Response Time: {response['response_time']} seconds")

# You can also check for follow-up questions
if response['follow_up_questions']:
    print("\nFollow-up Questions:")
    for question in response['follow_up_questions']:
        print(f"- {question}")
else:
    print("\nNo follow-up questions provided.")

# You can also check for images
if response['images']:
    print("\nImages Found:")
    for image in response['images']:
        print(f"- {image}") # The structure of image data might vary
else:
    print("\nNo images found.")