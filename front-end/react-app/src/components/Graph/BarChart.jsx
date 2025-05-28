import React, { useState } from "react";
import Chart from 'react-apexcharts';
import styles from "./Graph.module.css";
  
export default function BarChart({title,y_axis_title,num_element,category_element}) {

    var options = {
      series: [{
      name: y_axis_title,
      data: num_element
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
      categories: category_element,
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
          text: y_axis_title
        }
    
    }
    };

    return (
    
      <div className={styles.graphContainer}>
        <div>
          <h1 style={{ textAlign: 'center',fontSize:'30px' }}>{title}</h1>
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
        </div>)
  }

