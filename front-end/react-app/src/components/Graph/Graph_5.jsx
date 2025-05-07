
  import React, { useState } from "react";
  import Chart from 'react-apexcharts';
  import styles from "./Graph.module.css";
  
  export function Graph_5() {
    var options = {
      series: [{
      name: "Number of Orders",
      data: [22, 25, 23, 26, 25, 31, 33, 11]
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
      categories: ['1996-07', '1996-08', '1996-09', '1996-10', '1996-11', '1996-12', '1997-01', '1997-02'],
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
          <h1 style={{ textAlign: 'center',fontSize:'30px' }}>Number of Orders per Month</h1>
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

  