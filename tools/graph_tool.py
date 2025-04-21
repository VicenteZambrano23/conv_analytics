import sqlite3
from pydantic import BaseModel, Field
from typing import Annotated, Literal

db_path = '/teamspace/studios/this_studio/conv_analytics/database/mydatabase.db'
class GraphInput(BaseModel):
    query: Annotated[str, Field(description="Query in SQLite")]
    title: Annotated[str, Field(description="Title for the graph")]

def graph_tool(input: Annotated[GraphInput, "Input to the graph tool."] ):
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
      series: [{{
      name: 'Count',
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
    dataLabels: {{
      enabled: true,
      formatter: function (val) {{
        return val;
      }},
      offsetY: -20,
      style: {{
        fontSize: '12px',
        colors: ["#304758"]
      }}
    }},
    
    xaxis: {{
      categories: {category_element},
      position: 'top',
      axisBorder: {{
        show: false
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
        show: false
      }},
      axisTicks: {{
        show: false,
      }},
      labels: {{
        show: false,
        formatter: function (val) {{
          return val;
        }}
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
  except Exception as e:
    print(f"An error occurred: {e}")