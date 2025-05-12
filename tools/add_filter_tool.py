import sqlite3
from pydantic import BaseModel, Field
from typing import Annotated, Literal
from utils.summary_func import summary_query
from config.config import db_path
from utils.update_counter import update_counter, get_counter
from utils.update_graph import update_graph
from utils.get_graph_data import get_graph_data


class FilterInput(BaseModel):
    graphic_number: Annotated[
        int, Field(description="Position when the graphic is generated")
    ]


def add_filter_tool(
    input: Annotated[FilterInput, "Input to the graph bar filter tool."],
):

    counter = input.graphic_number
    data = get_graph_data(counter)
    type = data["type"]
    query = data["query"]
    title = data["title"]
    if type == "bar":

        y_axis_title = data["y_axis_title"]

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute(query)
        query_result = cursor.fetchall()
        category_element = [item[0] for item in query_result]
        num_element = [item[1] for item in query_result]

        jsx_code = f"""
    import React, {{ useState }} from "react";
    import Chart from 'react-apexcharts';
    import styles from "./Graph.module.css";
    import Box from '@mui/material/Box';
    import Slider from '@mui/material/Slider';
    
    export function Graph_{counter}() {{

      function valuetext(value) {{
          return `${{value}}°C`;
        }}
    const data = {num_element}
    const dataCategory = {category_element}
    const [dataVisual,setDataVisual] = useState(data)
    const [dataCategoryVisual,setDataCategoryVisual] = useState(dataCategory)
    const [value, setValue] = useState([Math.min(...data), Math.max(...data)]);
        
    const handleChange = (event, newValue) => {{
        const filteredData = data.filter(item => item >= Math.min(...newValue) && item <= Math.max(...newValue));
        setDataVisual(filteredData);
    
        // Create a Set to store unique categories
        const uniqueCategories = new Set();
    
        // Iterate through the original data and categories
        data.forEach((item, index) => {{
          if (item >= Math.min(...newValue) && item <= Math.max(...newValue)) {{
            uniqueCategories.add(dataCategory[index]);
          }}
        }});
    
        setDataCategoryVisual(Array.from(uniqueCategories));
        setValue(newValue);
          }};

      var options = {{
        series: [{{
        name: "{y_axis_title}",
        data: dataVisual,
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
        categories: dataCategoryVisual,
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
          <div className={{styles.filterContainer}}>
          <Box sx={{{{ width: 300 }}}}>
    <Slider
      getAriaLabel={{() => 'Temperature range'}}
      value={{value}}
      onChange={{handleChange}}
      valueLabelDisplay="auto"
      getAriaValueText={{valuetext}}
      min={{Math.min(...data)}}
      max={{Math.max(...data)}}
    />
  </Box>
  <h4>{y_axis_title}</h4>
  </div>
          </div>)
    }}

    """

        try:
            with open(
                f"/teamspace/studios/this_studio/conv_analytics/front-end/react-app/src/components/Graph/Graph_{str(counter)}.jsx",
                "w",
            ) as file:
                file.write(jsx_code)

            update_graph()
            return f"Filter of bar graph correctly added. Filter numeric range in {y_axis_title}"
        except Exception as e:
            print(f"An error occurred: {e}")
