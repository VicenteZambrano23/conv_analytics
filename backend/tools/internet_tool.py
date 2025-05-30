from pydantic import BaseModel, Field
from typing import Annotated, Literal
from utils.summary_func import summary_query
from config.config import db_path
from tavily import TavilyClient
from config.config import TAVILY_API_KEY


class InternetInput(BaseModel):
    message: Annotated[str, "query that can be used to retrieve content from internet."]
    n_results: Annotated[int, "number of results"] = 10


def internet_tool(input: Annotated[InternetInput, "Input to the internet tool."]):

    # Tavily API to perform the internet Search
    tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
    response = tavily_client.search(
        input.message,
        include_answer="advanced",
        max_results=input.n_results,
        search_depth="advanced",
    )  # , include_raw_content= True) # Perform the internet search

    # Crear un nuevo diccionario para el JSON simplificado
    info = {}

    # Añadir la respuesta principal
    info["answer"] = response["answer"]

    # Crear una lista para almacenar los diccionarios de URL y título
    urls_with_titles = []
    for result in response["results"][
        :2
    ]:  # Crear un diccionario para cada par de URL y título
        url_info = {"title": result["title"], "url": result["url"]}
        urls_with_titles.append(url_info)

    # Añadir la lista de URLs con títulos al nuevo JSON
    info["urls"] = urls_with_titles

    # Imprimir el nuevo JSON de forma legible
    import json

    print(json.dumps(info, indent=4))

    return info
