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
  connection.close()
  category_element = [item[0] for item in query_result]
  category_unique = list(set(category_element))

  group_element = [item[1] for item in query_result]
  group_unique = list(set(group_element))


  result = {}

  for category in category_unique:
      category_data = [item for item in query_result if item[0] == category]
      group_values = {}
      for cat, group, value in category_data:
          group_values[group] = value

      group_numbers = []
      for group in group_unique:
          group_numbers.append(group_values.get(group, 0))
      result[category] = group_numbers

  output_string = ""
  for key, value in result.items():
      output_string += f"""\
      {{
          name: '{key}',
          data: {value}
      }},
  """
  colors = ['#008000', '#FF0000', '#0000FF',"#FFFF00"]

  jsx_code = f"""
  import React, {{ useState }} from "react";
  import Chart from 'react-apexcharts';

  export function Graph() {{
    return (
      <Chart
    type='bar'
    width={{600}}
    height={{600}}
    series={{[
      {output_string}
    ]}}
    options={{{{
      colors: {colors}, // Added a second color for the second series
      chart: {{
        height: 600, // Adjusted to your chart height
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
          return val; // Removed the percentage as your data doesn't seem to be percentages
        }},
        offsetY: -20,
        style: {{
          fontSize: '12px',
          colors: ["#304758"]
        }}
      }},

      xaxis: {{
        categories: {group_unique}, // Added some categories
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
          }},
          tooltip: {{
            enabled: true,
          }}
        }},
      }},
      yaxis: {{
        axisBorder: {{
          show: false
        }},
        axisTicks: {{
          show: false,
        }},
        labels: {{
          show: true, // Changed to true to show labels
          // formatter: function (val) {{ // Removed percentage formatting as data isn't percentage
          //   return val + "%";
          // }}
        }}

      }},
      title: {{
        text: '{title}', // Updated title
        floating: false,
        // Changed to false to position the title normally
        offsetY: 0,
        align: 'center',
        style: {{
          color: '#444'
        }}
      }}
    }}}}
  ></Chart>
    );
  }}

  """

  try:
    with open('/teamspace/studios/this_studio/conv_analytics/front-end/react-app/src/components/Graph/Graph.jsx', 'w') as file:
      file.write(jsx_code)
  except Exception as e:
    print(f"An error occurred: {e}")