import os

from dotenv import load_dotenv

load_dotenv()

AZURE_OPENAI_CONFIG = {
    "config_list": [
        {
            "model": os.getenv("DEPLOYMENT_NAME"),
            "api_key": os.getenv("AZURE_OPENAI_API_KEY"),
            "api_type": "azure",
            "base_url": os.getenv("AZURE_OPENAI_ENDPOINT"),
            "api_version": os.getenv("API_VERSION"),
        }
    ],
}

db_path = os.path.join(os.path.dirname(__file__), "..", "database/mydatabase.db")

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
