import os

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

db_path = '/teamspace/studios/this_studio/conv_analytics/database/mydatabase.db'