import sqlite3
from pydantic import BaseModel, Field
from typing import Annotated, Literal
from utils.summary_func import summary_query
from config.config import db_path
from utils.update_counter import update_counter, get_counter
from utils.update_graph import update_graph
from utils.get_graph_data import get_graph_data
from utils.update_json_fields import update_json_fields

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


      update_json_fields(str(counter),"filter_added", True)
       

        
    elif type == "scatter":

      y_axis= data["y_axis"]
      x_axis = data["x_axis"]

      connection = sqlite3.connect(db_path)
      cursor = connection.cursor()
      cursor.execute(query)
      data_dict = {}
      rows = cursor.fetchall()

      if len(rows[0]) == 3:

          for row in rows:
              category = row[0]
              value_1 = row[1]
              value_2 = row[2]

              if category not in data_dict:
                  data_dict[category] = []
              data_dict[category].append([value_1, value_2])

      else:
          data_dict["value"] = []
          for row in rows:
              value_1 = row[0]
              value_2 = row[1]

              data_dict["value"].append([value_1, value_2])

      output_string = ""

      for key, value in data_dict.items():
          output_string += f"""\
      {{
            name: "{key}",
            data: {value}
      }},
      """
      jsx_code = f"""
        import Chart from 'react-apexcharts';
import styles from "./Graph.module.css";
import Box from '@mui/material/Box';
import Slider from '@mui/material/Slider';
import {{ useState }} from "react";

export function Graph_{counter}() {{
   const initialData = [{output_string}];

   function valuetext(value) {{
     return `${{value}}`; // Removed extra curly braces
  }}

  const [data, setData] = useState(initialData);
  const [dataVisual, setDataVisual] = useState(initialData);
  const [dataCategoryVisual, setDataCategoryVisual] = useState(initialData.map(item => item.name));
  const [value1, setValue1] = useState([
  Math.min(...initialData.map(item => item.data[0][0])),
  Math.max(...initialData.map(item => item.data[0][0])),
  ]);
  const [value2, setValue2] = useState([
  Math.min(...initialData.map(item => item.data[0][1])),
  Math.max(...initialData.map(item => item.data[0][1])),
  ]);

   const handleChangeSlicer1 = (event, newValue) => {{
    setValue1(newValue);
    filterData(newValue, value2);
   }};

   const handleChangeSlicer2 = (event, newValue) => {{
     setValue2(newValue);
     filterData(value1, newValue);
   }};

  const filterData = (range1, range2) => {{
  const filteredData = initialData.filter(item => {{ // Use initialData for filtering
  const firstValue = item.data[0][0];
  const secondValue = item.data[0][1];
  return firstValue >= range1[0] && firstValue <= range1[1] &&
  secondValue >= range2[0] && secondValue <= range2[1];
 }});
   setDataVisual(filteredData);
    const uniqueCategories = [...new Set(filteredData.map(item => item.name))];
    setDataCategoryVisual(uniqueCategories);
   }};

   const chartData = dataVisual.map(item => ({{
    name: item.name,
    data: item.data
   }}));

   var options = {{
     colors: ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"],
     series: chartData, // Use the processed chartData
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
     }},
      }},
     yaxis: {{
    labels: {{
     formatter: function(val) {{
       return parseFloat(val).toFixed(1)
     }}
     }},
     tickAmount: 7,
     title: {{
       text: '{y_axis}'
       }}
    }}
   }};

  return (
    <div className={{styles.graphContainer}}>
  <div>
    <h1 style={{{{ textAlign: 'center', fontSize: '30px' }}}}>
      {title}
    </h1>
  </div>
  <div className={{styles.graphSubContainer}}>
    <Chart
      type='scatter'
      width='220%' // Adjusted width to be responsive within its container
      height='95%'
      series={{options.series}}
      options={{options}}
    />
  </div>
  <div className={{styles.filterContainer}}>
    <Box sx={{{{ width: '25vw' }}}}>
      <Slider
        getAriaLabel={{() => '{x_axis}'}} // More descriptive label
        value={{value1}}
        onChange={{handleChangeSlicer1}}
        valueLabelDisplay="auto"
        getAriaValueText={{valuetext}}
        min={{Math.min(...initialData.map(item => item.data[0][0]))}} // Use initialData for min/max
        max={{Math.max(...initialData.map(item => item.data[0][0]))}} // Use initialData for min/max
      />
    </Box>
    <h4>{x_axis}</h4>
  </div>
  <div className={{styles.filterContainer}}>
    <Box sx={{{{ width: '25vw' }}}}>
      <Slider
        getAriaLabel={{() => '{y_axis}'}} // More descriptive label
        value={{value2}}
        onChange={{handleChangeSlicer2}}
        valueLabelDisplay="auto"
        getAriaValueText={{valuetext}}
        min={{Math.min(...initialData.map(item => item.data[0][1]))}} // Use initialData for min/max
        max={{Math.max(...initialData.map(item => item.data[0][1]))}} // Use initialData for min/max
      />
    </Box>
    <h4>{y_axis}</h4>
  </div>
</div>
  );
}}
      

      """

      try:
        with open(f"/teamspace/studios/this_studio/conv_analytics/front-end/react-app/src/components/Graph/Graph_{str(counter)}.jsx","w",) as file:
          file.write(jsx_code)

        
        return f"Filter of scatter graph correctly added. Filter numeric range in {y_axis} and {x_axis}"

      except Exception as e:
              print(f"An error occurred: {e}")


    elif type == "line":

      y_axis_title= data["y_axis_title"]
      x_axis_title = data["x_axis_title"]

      connection = sqlite3.connect(db_path)
      cursor = connection.cursor()
      cursor.execute(query)
      query_result = cursor.fetchall()

      category_element = [item[0] for item in query_result]
      num_element = [item[1] for item in query_result]

      jsx_code = f"""
        import React, {{ useState, useEffect }} from "react";
        import Chart from 'react-apexcharts';
        import styles from "./Graph.module.css";
        import DatePicker from "react-datepicker";

        import "react-datepicker/dist/react-datepicker.css";

        export function Graph_{counter}() {{
          // Original data and dates
          const originalData = {num_element};
          const originalDates = {category_element};
          
          // Convert string dates to Date objects for comparison
          const dateObjects = originalDates.map(dateStr => {{
            const [year, month] = dateStr.split('-');
            return new Date(parseInt(year), parseInt(month) - 1, 1);
          }});
          
          // Get min and max dates from the dataset
          const minDate = new Date(Math.min(...dateObjects));
          const maxDate = new Date(Math.max(...dateObjects));
          
          // State for filtered data
          const [data, setData] = useState(originalData);
          const [dates, setDates] = useState(originalDates);
          
          // State for date pickers
          const [startDate, setStartDate] = useState(minDate);
          const [endDate, setEndDate] = useState(maxDate);
          
          // Filter data when date range changes
          useEffect(() => {{
            filterDataByDateRange();
          }}, [startDate, endDate]);
          
          // Function to handle start date change
          const handleStartDateChange = (date) => {{
            setStartDate(date);
          }};
          
          // Function to handle end date change
          const handleEndDateChange = (date) => {{
            setEndDate(date);
          }};
          
          // Function to filter data by date range
          const filterDataByDateRange = () => {{
            const filteredIndexes = [];
            
            dateObjects.forEach((date, index) => {{
              if (date >= startDate && date <= endDate) {{
                filteredIndexes.push(index);
              }}
            }});
            
            const filteredData = filteredIndexes.map(index => originalData[index]);
            const filteredDates = filteredIndexes.map(index => originalDates[index]);
            
            setData(filteredData);
            setDates(filteredDates);
          }};
          
          var options = {{
            series: [{{
              name: '{y_axis_title}',
              data: data
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
              categories: dates,
              title: {{
                text: '{x_axis_title}'
              }}
            }},
            yaxis: {{
              title: {{
                text: '{y_axis_title}'
              }}
            }}
          }};

          return (
            <div className={{styles.graphContainer}}>
              <div>
                <h1 style={{{{ textAlign: 'center', fontSize:'30px' }}}}>{title}</h1>
              </div>
              <div className={{styles.graphSubContainer}}>
                <Chart
                  type='line'
                  width='220%'
                  height='95%' 
                  series={{options.series}}
                  options={{options}}
                  align='center'
                ></Chart>
              </div>
              <div className={{styles.dateContainer}}>
                <DatePicker
                  selected={{startDate}}
                  onChange={{handleStartDateChange}}
                  dateFormat="yyyy-MM"
                  showMonthYearPicker
                  placeholderText="Start Date"
                />
                <h4 style={{{{'marginLeft':'2vw', 'marginRight':'2vw'}}}}>to</h4> 
                <DatePicker
                  selected={{endDate}}
                  onChange={{handleEndDateChange}}
                  dateFormat="yyyy-MM"
                  showMonthYearPicker
                  placeholderText="End Date"
                  minDate={{startDate}}
                />
              </div>
            </div>
          )
        }}

      """
      try:
        with open(f"/teamspace/studios/this_studio/conv_analytics/front-end/react-app/src/components/Graph/Graph_{str(counter)}.jsx","w",) as file:
          file.write(jsx_code)

        
        return f"Filter of line graph correctly added. Filter date range in {x_axis_title}"

      except Exception as e:
              print(f"An error occurred: {e}")

    elif type == "bar_line":

      
      if query.find("SELECT") == -1:
          return "Not SELECT statement"

      y_bar_axis_title = data['y_bar_axis_title']
      y_line_axis_title = data['y_line_axis_title']

      connection = sqlite3.connect(db_path)
      cursor = connection.cursor()
      cursor.execute(query)
      query_result = cursor.fetchall()

      category_element = [item[0] for item in query_result]
      num_element_bar = [item[1] for item in query_result]
      num_element_line = [item[2] for item in query_result]

      jsx_code = f"""
        import React, {{ useState, useEffect }} from "react";
        import Chart from 'react-apexcharts';
        import styles from "./Graph.module.css";
        import DatePicker from "react-datepicker";

        import "react-datepicker/dist/react-datepicker.css";

        export function Graph_{counter}() {{
          // Original data and dates
          const originalOrdersData = {num_element_bar};
          const originalRevenueData = {num_element_line};
          const originalLabels = {category_element};
          
          // State for filtered data
          const [ordersData, setOrdersData] = useState(originalOrdersData);
          const [revenueData, setRevenueData] = useState(originalRevenueData);
          const [labels, setLabels] = useState(originalLabels);
          
          // Convert string dates to Date objects for comparison
          const dateObjects = originalLabels.map(dateStr => {{
            const [year, month] = dateStr.split('-');
            return new Date(parseInt(year), parseInt(month) - 1, 1);
          }});
          
          // Get min and max dates from the dataset
          const minDate = new Date(Math.min(...dateObjects));
          const maxDate = new Date(Math.max(...dateObjects));
          
          // State for date pickers
          const [startDate, setStartDate] = useState(minDate);
          const [endDate, setEndDate] = useState(maxDate);
          
          // Filter data when date range changes
          useEffect(() => {{
            filterDataByDateRange();
          }}, [startDate, endDate]);
          
          // Function to handle start date change
          const handleStartDateChange = (date) => {{
            setStartDate(date);
          }};
          
          // Function to handle end date change
          const handleEndDateChange = (date) => {{
            setEndDate(date);
          }};
          
          // Function to filter data by date range
          const filterDataByDateRange = () => {{
            const filteredIndexes = [];
            
            dateObjects.forEach((date, index) => {{
              if (date >= startDate && date <= endDate) {{
                filteredIndexes.push(index);
              }}
            }});
            
            const filteredOrdersData = filteredIndexes.map(index => originalOrdersData[index]);
            const filteredRevenueData = filteredIndexes.map(index => originalRevenueData[index]);
            const filteredLabels = filteredIndexes.map(index => originalLabels[index]);
            
            setOrdersData(filteredOrdersData);
            setRevenueData(filteredRevenueData);
            setLabels(filteredLabels);
          }};

          var options = {{
            series: [{{
              name: "{y_bar_axis_title}",
              type: 'column',
              data: ordersData
            }}, {{
              name: "{y_line_axis_title}",
              type: 'line',
              data: revenueData,
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
            labels: labels,
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
            <div className={{styles.graphContainer}}>
              <div>
                <h1 style={{{{ textAlign: 'center', fontSize:'30px' }}}}>{title}</h1>
              </div>
              <div className={{styles.graphSubContainer}}>
                <Chart
                  type='bar'
                  width='220%'
                  height='95%'
                  series={{options.series}}
                  options={{options}}
                  align='center'
                ></Chart>
              </div>
              <div className={{styles.dateContainer}}>
                <DatePicker
                  selected={{startDate}}
                  onChange={{handleStartDateChange}}
                  dateFormat="yyyy-MM"
                  showMonthYearPicker
                  placeholderText="Start Date"
                />
                <h4 style={{{{'marginLeft':'2vw', 'marginRight':'2vw'}}}}>to</h4> 
                <DatePicker
                  selected={{endDate}}
                  onChange={{handleEndDateChange}}
                  dateFormat="yyyy-MM"
                  showMonthYearPicker
                  placeholderText="End Date"
                  minDate={{startDate}}
                />
              </div>
            </div>
          );
      }}

      """
      try:
        with open(f"/teamspace/studios/this_studio/conv_analytics/front-end/react-app/src/components/Graph/Graph_{str(counter)}.jsx","w",) as file:
          file.write(jsx_code)

        
        return f"Filter of line-bar graph correctly added. Filter date range by month"

      except Exception as e:
              print(f"An error occurred: {e}")


