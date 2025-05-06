import sqlite3
from pydantic import BaseModel, Field
from typing import Annotated, Literal
from utils.summary_func import summary_query
from config.config import db_path
from utils.update_counter import update_counter, get_counter
from utils.update_graph import update_graph
class GraphBarLineInput(BaseModel):
    query: Annotated[str, Field(description="Query in SQLite")]
    title: Annotated[str, Field(description="Title for the graph")]
    y_bar_axis_title: Annotated[str, Field(description="Title for the y1-axis")]
    y_line_axis_title: Annotated[str, Field(description="Title for the y2-axis")]

def graph_bar_line_tool(input: Annotated[GraphBarLineInput, "Input to the graph bar line tool."] ):

  query = input.query
  if query.find('SELECT') == -1:
    return "Not SELECT statement"

  update_counter()
  counter = get_counter()
  title = input.title
  y_bar_axis_title = input.y_bar_axis_title
  y_line_axis_title = input.y_line_axis_title

  if query.find('LIMIT') == -1:
    query = query.replace(';'," ")
    
    query += " LIMIT 10;"
  else:
    query = query
  

  connection = sqlite3.connect(db_path)
  cursor = connection.cursor()
  cursor.execute(query)
  query_result = cursor.fetchall()
  print(query_result)
  query_summary = summary_query(str(query_result))
  category_element = [item[0] for item in query_result]
  num_element_bar= [item[1] for item in query_result]
  num_element_line= [item[2] for item in query_result]
  print(num_element_bar)
  print(num_element_line)
  jsx_code = f"""
  import React, {{ useState }} from "react";
  import Chart from 'react-apexcharts';

  export function Graph_{counter}() {{
    var options = {{
          series: [{{
          name: "{y_bar_axis_title}",
          type: 'column',
          data: {num_element_bar}
        }}, {{
          name: "{y_line_axis_title}",
          type: 'line',
          data: {num_element_line},
        }}],
          chart: {{
          height: 350,
          type: 'line',
        }},
        stroke: {{
          width: [0, 4]
        }},
        markers: {{
          shape: 'square',
          size: 12
        }},
        dataLabels: {{
          enabled: true,
          enabledOnSeries: [1],
          formatter: function (val) {{
            return val.toFixed(0);
          }},
        }},
        labels: {category_element},
        yaxis: [{{
          title: {{
            text: "{y_bar_axis_title}",
          }},
          labels: {{
            formatter: function (val) {{
              return val.toFixed(0);
            }}
          }}
        }}, {{
          opposite: true,
          title: {{
            text: "{y_line_axis_title}",
          }},
          labels: {{
            formatter: function (val) {{
              return val.toFixed(0);
            }}
          }}
        }}]
        }};

    return (
      <div style={{{{ textAlign: 'center' }}}}>
      <h1 style={{{{ textAlign: 'center',fontSize:'35px' }}}}>{title}</h1>
      <Chart
      type='bar'
      width={{750}} // Adjusted width to match your options
      height={{475}} // Adjusted height to match your options
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
    return f"Bar graph correctly added. Title: {title}. Y-bar-axis title: {y_bar_axis_title}. Y-line-axis title: {y_bar_axis_title} Data:{query_summary}"
  except Exception as e:
    print(f"An error occurred: {e}")

