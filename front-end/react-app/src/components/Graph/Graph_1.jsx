
    import React, { useState } from "react";
    import Chart from 'react-apexcharts';
    import styles from "./Graph.module.css";
    import Box from '@mui/material/Box';
    import Slider from '@mui/material/Slider';
    
    export function Graph_1() {

      function valuetext(value) {
          return `${value}°C`;
        }
    const data = [10, 7, 7, 7, 6, 6, 5, 5, 5, 4]
    const dataCategory = ['Ernst Handel', 'Wartian Herkku', 'Rattlesnake Canyon Grocery', 'QUICK-Stop', 'Split Rail Beer & Ale', 'Hungry Owl All-Night Grocers', 'Mère Paillarde', "La maison d''Asie", 'LILA-Supermercado', 'Tortuga Restaurante']
    const [dataVisual,setDataVisual] = useState(data)
    const [dataCategoryVisual,setDataCategoryVisual] = useState(dataCategory)
    const [value, setValue] = useState([Math.min(...data), Math.max(...data)]);
        
    const handleChange = (event, newValue) => {
        const filteredData = data.filter(item => item >= Math.min(...newValue) && item <= Math.max(...newValue));
        setDataVisual(filteredData);
    
        // Create a Set to store unique categories
        const uniqueCategories = new Set();
    
        // Iterate through the original data and categories
        data.forEach((item, index) => {
          if (item >= Math.min(...newValue) && item <= Math.max(...newValue)) {
            uniqueCategories.add(dataCategory[index]);
          }
        });
    
        setDataCategoryVisual(Array.from(uniqueCategories));
        setValue(newValue);
          };

      var options = {
        series: [{
        name: "Number of Orders",
        data: dataVisual,
        }],
        chart: {
        height: 350,
        type: 'bar',
        },
      plotOptions: {
        bar: {
          borderRadius: 10,
          dataLabels: {
            position: 'top', // top, center, bottom
          },
        }
      },
      
      
      xaxis: {
        categories: dataCategoryVisual,
        position: 'bottom',
        axisBorder: {
          show: true
        },
        axisTicks: {
          show: false
        },
        crosshairs: {
          fill: {
            type: 'gradient',
            gradient: {
              colorFrom: '#D8E3F0',
              colorTo: '#BED1E6',
              stops: [0, 100],
              opacityFrom: 0.4,
              opacityTo: 0.5,
            }
          }
        },
        tooltip: {
          enabled: true,
        }
      },
      yaxis: {
        axisBorder: {
          show: true
        },
        axisTicks: {
          show: true,
        },
        labels: {
          show: true,
          formatter: function (val) {
            return val;
          }
        },
        title: {
            text: "Number of Orders"
          }
      
      }
      };

      return (
      
        <div className={styles.graphContainer}>
          <div>
            <h1 style={{ textAlign: 'center',fontSize:'30px' }}>Top 10 Customers by Number of Orders</h1>
          </div>
          <div className={styles.graphSubContainer}>
            <Chart
            type='bar'
            width='220%'
            height='95%' 
            series={options.series}
            options={options}
            align= 'center'>
            </Chart>
          </div>
          <div className={styles.filterContainer}>
          <Box sx={{ width: 300 }}>
    <Slider
      getAriaLabel={() => 'Temperature range'}
      value={value}
      onChange={handleChange}
      valueLabelDisplay="auto"
      getAriaValueText={valuetext}
      min={Math.min(...data)}
      max={Math.max(...data)}
    />
  </Box>
  <h4>Number of Orders</h4>
  </div>
          </div>)
    }

    