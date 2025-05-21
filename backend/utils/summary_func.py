from openai import AzureOpenAI
from config.config import AZURE_OPENAI_CONFIG, db_path

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_key=AZURE_OPENAI_CONFIG['config_list'][0]['api_key'],
    api_version=AZURE_OPENAI_CONFIG['config_list'][0]['api_version'],
    azure_endpoint=AZURE_OPENAI_CONFIG['config_list'][0]['base_url'],
)

def summary_query(query_result: str) :
   
    system_prompt = (
        """
        Your task is to summary the results of a query in Natural Language
        """
    )

    user_prompt = f"""
        Summary the query in Natural Language and retrieve the results in markdown. **Don´t mention is a query, just explain the data.
        The data obtained by the query is the following: 
        {query_result}

    """

    
    response = client.chat.completions.create(
        model=AZURE_OPENAI_CONFIG['config_list'][0]['model'],
        messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
        ],
        temperature=0.5,
        max_tokens=400,
    )
    summary_query = response.choices[0].message.content
        
    return summary_query
            


