import sqlite3
from pydantic import BaseModel, Field
from typing import Annotated, Literal

db_path = '/teamspace/studios/this_studio/conv_analytics/database/mydatabase.db'
class GraphInput(BaseModel):
    query: Annotated[str, Field(description="Query in SQLite")]
    title: Annotated[str, Field(description="Title for the graph")]

def graph_pie_tool(input: Annotated[GraphInput, "Input to the graph tool."] ):
  query = input.query
  title = input.title

  connection = sqlite3.connect(db_path)
  cursor = connection.cursor()
  cursor.execute(query)
  query_result = cursor.fetchall()
  category_element = [item[0] for item in query_result]
  num_element= [item[1] for item in query_result]

  jsx_code = f"""
  import React, {{ useState }} from "react";
import Chart from 'react-apexcharts';

 export function Graph() {{
 var options = {{
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
    with open('/teamspace/studios/this_studio/conv_analytics/front-end/react-app/src/components/Graph/Graph.jsx', 'w') as file:
      file.write(jsx_code)
  except Exception as e:
    print(f"An error occurred: {e}")