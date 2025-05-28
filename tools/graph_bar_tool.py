import sqlite3
from pydantic import BaseModel, Field
from typing import Annotated, Literal
from utils.summary_func import summary_query
from config.config import db_path
from utils.update_counter import update_counter, get_counter
from utils.update_graph import update_graph
import json
from utils.update_graph_data import update_graph_data


class GraphBarInput(BaseModel):
    query: Annotated[str, Field(description="Query in SQLite")]
    title: Annotated[str, Field(description="Title for the graph")]
    y_axis_title: Annotated[str, Field(description="Title for the y-axis")]


def graph_bar_tool(input: Annotated[GraphBarInput, "Input to the graph bar tool."]):
    query = input.query
    if query.find("SELECT") == -1:
        return "Not SELECT statement"


    title = input.title
    y_axis_title = input.y_axis_title

    counter = get_counter()
    if query.find("LIMIT") == -1:
        query = query.replace(";", " ")

        query += " LIMIT 10;"
    else:
        query = query

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
  
  export function Graph_{counter + 1}() {{
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
    
      <div className={{styles.graphContainer}}>
        <div>
          <h1 style={{{{ textAlign: 'center',fontSize:'30px' }}}}>{title}</h1>
        </div>
        <div className={{styles.graphSubContainer}}>
          <Chart
          type='bar'
          width='220%'
          height='95%' 
          series={{options.series}}
          options={{options}}
          align= 'center'>
          </Chart>
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


        
        update_counter()
        graph_data = {
            str(counter+1): {
                "type": "bar",
                "query": query,
                "title": title,
                "y_axis_title": y_axis_title,
                "x_axis": category_element,
                "y_axis":num_element,
                "filter_added": "No"
            }
        }

        update_graph_data(graph_data)
        return f"Bar graph correctly added. Title: {title}. Y-axis title: {y_axis_title}. Data:{query_summary}"
    except Exception as e:
        print(f"An error occurred: {e}")
