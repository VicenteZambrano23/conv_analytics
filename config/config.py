import os
from dotenv import load_dotenv

load_dotenv()


AZURE_OPENAI_CONFIG = {
    "config_list": [
        {
            "model": os.environ.get("DEPLOYMENT_NAME"),
            "api_key": os.environ.get("AZURE_OPENAI_API_KEY"),
            "api_type": "azure",
            "base_url": os.environ.get("AZURE_OPENAI_ENDPOINT"),
            "api_version": os.environ.get("API_VERSION"),
        }
    ],
}

db_path  = os.path.join(
    os.path.dirname(__file__), "..", "database/mydatabase.db"
)