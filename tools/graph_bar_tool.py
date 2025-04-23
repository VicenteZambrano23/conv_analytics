import sqlite3
from pydantic import BaseModel, Field
from typing import Annotated, Literal

db_path = '/teamspace/studios/this_studio/conv_analytics/database/mydatabase.db'
class GraphBarInput(BaseModel):
    query: Annotated[str, Field(description="Query in SQLite")]
    title: Annotated[str, Field(description="Title for the graph")]
    y_axis_title: Annotated[str, Field(description="Title for the y-axis")]

def graph_bar_tool(input: Annotated[GraphBarInput, "Input to the graph bar tool."] ):
  
  query = input.query
  title = input.title
  y_axis_title = input.y_axis_title

  if query.find('LIMIT') == -1:
    query = query.replace(';'," ")
    
    query += " LIMIT 10;"
  else:
    query = query
  

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
      series: [{{
      name: "{y_axis_title}",
      data: {num_element}
      }}],
      chart: {{
      height: 350,
      type: 'bar',
      }},
    plotOptions: {{
      bar: {{
        borderRadius: 10,
        dataLabels: {{
          position: 'top', // top, center, bottom
        }},
      }}
    }},
    
    
    xaxis: {{
      categories: {category_element},
      position: 'bottom',
      axisBorder: {{
        show: true
      }},
      axisTicks: {{
        show: false
      }},
      crosshairs: {{
        fill: {{
          type: 'gradient',
          gradient: {{
            colorFrom: '#D8E3F0',
            colorTo: '#BED1E6',
            stops: [0, 100],
            opacityFrom: 0.4,
            opacityTo: 0.5,
          }}
        }}
      }},
      tooltip: {{
        enabled: true,
      }}
    }},
    yaxis: {{
      axisBorder: {{
        show: true
      }},
      axisTicks: {{
        show: true,
      }},
      labels: {{
        show: true,
        formatter: function (val) {{
          return val;
        }}
      }},
      title: {{
          text: "{y_axis_title}"
        }}
    
    }}
    }};

    return (
      <div style={{{{ textAlign: 'center' }}}}>
      <h1 style={{{{ textAlign: 'center' }}}}>{title}</h1>
      <Chart
      type='bar'
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
    
    return "Bar graph correctly added"
  except Exception as e:
    print(f"An error occurred: {e}")

