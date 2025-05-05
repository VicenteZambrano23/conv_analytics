import sqlite3
from pydantic import BaseModel, Field, config
from typing import Annotated, Literal
from utils.summary_func import summary_query
from config.config import db_path
from utils.update_counter import update_counter, get_counter
from utils.update_graph import update_graph
class GraphLineInput(BaseModel):
    query: Annotated[str, Field(description="Query in SQLite")]
    title: Annotated[str, Field(description="Title for the graph")]
    y_axis_title: Annotated[str, Field(description="Title for the y-axis")]
    x_axis_title: Annotated[str, Field(description="Title for the x-axis")]

def graph_line_tool(input: Annotated[GraphLineInput, "Input to the graph line tool."] ):

  query = input.query

  if query.find('SELECT') == -1:
    return "Not SELECT statement"

  update_counter()
  counter = get_counter()

  title = input.title
  y_axis_title = input.y_axis_title
  x_axis_title = input.x_axis_title

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
import styles from "./Graph.module.css";

 export function Graph_{counter}() {{
 var options = {{
 series: [{{
 name: "{y_axis_title}",
data: {num_element}
 }}],
 chart: {{
 height: 350,
 type: 'line',
 zoom: {{
 enabled: false
 }}
  }},
 dataLabels: {{
enabled: false
 }},
 stroke: {{
curve: 'smooth',
colors: ['#008FFB']
 }},

 grid: {{
row: {{
colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
 opacity: 0.5
}},
 }},
 xaxis: {{
categories: {category_element},
title: {{
  text: '{x_axis_title}'
}}
 }},
 yaxis :{{
  title :{{
    text: "{y_axis_title}"
  }}
 }}
 }};

 return (
    <div className={{styles.graphContainer}}>
      <div>
        <h1 style={{{{ textAlign: 'center',fontSize:'30px' }}}}>{title}</h1>
      </div>
      <div  className={{styles.graphSubContainer}}>
        <Chart
        type= 'line'
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
    return f"Line graph correctly added. Title: {title}. Y-axis title: {y_axis_title}.X-axis title: {x_axis_title} Data:{query_summary}"
  except Exception as e:
    print(f"An error occurred: {e}")