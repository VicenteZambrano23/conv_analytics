import sqlite3
from pydantic import BaseModel, Field
from typing import Annotated, Literal

db_path = '/teamspace/studios/this_studio/conv_analytics/database/mydatabase.db'
class GraphInput(BaseModel):
    query: Annotated[str, Field(description="Query in SQLite")]
    title: Annotated[str, Field(description="Title for the graph")]
    x_axis: Annotated[str, Field(description="X-Axis name for the graph")]
    y_axis: Annotated[str, Field(description="Y-Axis name for the graph")]

def graph_scatter_tool(input: Annotated[GraphInput, "Input to the graph tool."] ):
  query= input.query
  title = input.title
  x_axis = input.x_axis
  y_axis = input.y_axis

  connection = sqlite3.connect(db_path)
  cursor = connection.cursor()
  cursor.execute(query)
  data_dict = {}
  rows = cursor.fetchall()

  for row in rows:
    category = row[0]
    value_1 = row[1]
    value_2 = row[2]

    if category not in data_dict:
        data_dict[category] = []
    data_dict[category].append([value_1, value_2])


  output_string = ""
  for key, value in data_dict.items():
    output_string += f"""\
    {{
          name: '{key}',
          data: {value}
    }},
    """
    
  jsx_code = f"""
import React, {{ useState }} from "react";
import Chart from 'react-apexcharts';

export function Graph() {{
var options = {{
 series: [{output_string}],
 chart: {{
 height: 350,
type: 'scatter',
zoom: {{
 enabled: true,
type: 'xy'
 }}
}},
xaxis: {{
 tickAmount: 10,
 labels: {{
 formatter: function(val) {{
 return parseFloat(val).toFixed(1)
 }}
 }},
 title: {{
          text: '{x_axis}'
        }}
}},
yaxis: {{
tickAmount: 7,
title: {{
          text: '{y_axis}'
        }}
}}
}};

return (
<div style={{{{ textAlign: 'center' }}}}>
<h1 style={{{{ textAlign: 'center' }}}}>{title}</h1>
<Chart
type= 'scatter'
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


