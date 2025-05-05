import sqlite3
from pydantic import BaseModel, Field
from typing import Annotated, Literal
from utils.summary_func import summary_query
from config.config import db_path
from utils.update_counter import update_counter, get_counter
from utils.update_graph import update_graph
class GraphScatterInput(BaseModel):
    query: Annotated[str, Field(description="Query in SQLite")]
    title: Annotated[str, Field(description="Title for the graph")]
    x_axis: Annotated[str, Field(description="X-Axis name for the graph")]
    y_axis: Annotated[str, Field(description="Y-Axis name for the graph")]

def graph_scatter_tool(input: Annotated[GraphScatterInput, "Input to the graph scatter tool."] ):

  query= input.query
  if query.find('SELECT') == -1:
    return "Not SELECT statement"
  
  update_counter()
  counter = get_counter()

  title = input.title
  x_axis = input.x_axis
  y_axis = input.y_axis

  connection = sqlite3.connect(db_path)
  cursor = connection.cursor()
  cursor.execute(query)
  data_dict = {}
  rows = cursor.fetchall()
  query_summary = summary_query(str(rows))


  if len(rows[0]) == 3:

    for row in rows:
      category = row[0]
      value_1 = row[1]
      value_2 = row[2]

      if category not in data_dict:
        data_dict[category] = []
      data_dict[category].append([value_1, value_2])

  else:
    data_dict['value'] = []
    for row in rows:
      value_1 = row[0]
      value_2 = row[1]

    
      data_dict['value'].append([value_1, value_2])

  output_string = ""
  
  for key, value in data_dict.items():
    output_string += f"""\
    {{
          name: "{key}",
          data: {value}
    }},
    """
    
  jsx_code = f"""
import React, {{ useState }} from "react";
import Chart from 'react-apexcharts';
import styles from "./Graph.module.css";

export function Graph_{counter}() {{
var options = {{
  colors: ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"],
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
          text: "{x_axis}"
        }}
}},
yaxis: {{
  labels: {{
    formatter: function(val) {{
    return parseFloat(val).toFixed(1)
    }}
    }},
tickAmount: 7,
title: {{
          text: "{y_axis}"
        }}
}}
}};

return (
      <div className={{styles.graphContainer}}>
        <div>
          <h1 style={{{{ textAlign: 'center',fontSize:'30px' }}}}>{title}</h1>
        </div>
        <div className={{styles.graphSubContainer}}>
          <Chart
          type= 'scatter'
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
    with open(f'/teamspace/studios/this_studio/conv_analytics/front-end/react-app/src/components/Graph/Graph_{str(counter)}.jsx', 'w') as file:
      file.write(jsx_code)
    update_graph()
    return f"Scatter graph correctly added.Title: {title}. Y-axis title: {y_axis}. X-axis: {x_axis} Data:{query_summary}"
  except Exception as e:
    print(f"An error occurred: {e}")

