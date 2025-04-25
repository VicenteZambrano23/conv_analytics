import sqlite3
from pydantic import BaseModel, Field
from typing import Annotated, Literal
from utils.summary_func import summary_query
from config.config import db_path
from utils.update_counter import update_counter, get_counter
from utils.update_graph import update_graph
class GraphPieInput(BaseModel):
    query: Annotated[str, Field(description="Query in SQLite")]
    title: Annotated[str, Field(description="Title for the graph")]

def graph_pie_tool(input: Annotated[GraphPieInput, "Input to the graph pie tool."] ):

  update_counter()
  counter = get_counter()

  query = input.query
  title = input.title

  connection = sqlite3.connect(db_path)
  cursor = connection.cursor()
  cursor.execute(query)
  query_result = cursor.fetchall()
  query_summary = summary_query(str(query_result))

  category_element = [item[0] for item in query_result]
  num_element= [item[1] for item in query_result]

  jsx_code = f"""
  import React, {{ useState }} from "react";
import Chart from 'react-apexcharts';

 export function Graph__{counter}() {{
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
<div style={{{{ textAlign: 'center' }}}}>
 <h1 style={{{{ textAlign: 'center' }}}}>{title}</h1>
 <Chart
 type= 'pie'
width={{800}} // Adjusted width to match your options
 height={{500}} // Adjusted height to match your options
 series={{options.series}}
 options={{options}}
 align= 'center'
 ></Chart></div>)
 }}

  """

  try:
    with open(f'/teamspace/studios/this_studio/conv_analytics/front-end/react-app/src/components/Graph/Graph_{str(counter)}.jsx', 'w') as file:
      file.write(jsx_code)
    update_graph()
    return f"Pie graph correctly added. Title: {title}. Data:{query_summary}"
  except Exception as e:
    print(f"An error occurred: {e}")