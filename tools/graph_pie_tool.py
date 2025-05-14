import sqlite3
from pydantic import BaseModel, Field
from typing import Annotated, Literal
from utils.summary_func import summary_query
from config.config import db_path
from utils.update_counter import update_counter, get_counter
from utils.update_graph import update_graph
from utils.update_graph_data import update_graph_data


class GraphPieInput(BaseModel):
    query: Annotated[str, Field(description="Query in SQLite")]
    title: Annotated[str, Field(description="Title for the graph")]


def graph_pie_tool(input: Annotated[GraphPieInput, "Input to the graph pie tool."]):

    query = input.query

    if query.find("SELECT") == -1:
        return "Not SELECT statement"

    counter = get_counter()

    title = input.title

    

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(query)
    query_result = cursor.fetchall()
    query_summary = summary_query(str(query_result))

    category_element = [item[0] for item in query_result]
    num_element = [item[1] for item in query_result]

    jsx_code = f"""
  import React, {{ useState }} from "react";
import Chart from 'react-apexcharts';
import styles from "./Graph.module.css";

 export function Graph_{counter+1}() {{
 var options = {{
  colors: ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"],
  series: {num_element},
  
labels:{category_element},
responsive: [{{
  breakpoint: 480,
  options: {{
    chart: {{
      width: 200
    }},
    legend: {{
      position: 'bottom'
    }}
  }}
}}],
dataLabels: {{
  enabled: true,
  formatter: function (val) {{
    return val.toFixed(1) + "%";
  }},
  style: {{
    colors: ['#fff'] // Set the text color to white
  }},
  dropShadow: {{
    enabled: true,
    top: 1,
    left: 1,
    blur: 2,
    color: '#000',
    opacity: 0.4
  }}
}},

    stroke: {{
      width: 2, // Adjust the width of the separation line (in pixels)
      color: '#000' // Set the color of the separation line (e.g., white)
    }},
}};

 return (
    <div className={{styles.graphContainer}}>
      <div>
        <h1 style={{{{ textAlign: 'center',fontSize:'30px' }}}}>{title}</h1>
      </div>
      <div className={{styles.graphSubContainer}}>
        <Chart
          type= 'pie'
          width='220%'
          height='95%' 
          series={{options.series}}
          options={{options}}
          align= 'center'
        ></Chart>
      </div>
    </div>)
 }}

  """

    try:
        with open(
            f"/teamspace/studios/this_studio/conv_analytics/front-end/react-app/src/components/Graph/Graph_{str(counter+1)}.jsx",
            "w",
        ) as file:
            file.write(jsx_code)
        update_graph()
        update_counter()

        title = input.title

        graph_data = {
            str(counter+1): {
                "type": "pie",
                "query": query,
                "title": title
            }
        }
        update_graph_data(graph_data)
        return f"Pie graph correctly added. Title: {title}. Data:{query_summary}"
    except Exception as e:
        print(f"An error occurred: {e}")
