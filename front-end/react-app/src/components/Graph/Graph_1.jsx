
  import React, { useState } from "react";
  import Chart from 'react-apexcharts';
  import styles from "./Graph.module.css";
  
  export function Graph_1() {
    var options = {
      series: [{
      name: "Total Revenue (USD)",
      data: [35631.21, 23362.6, 22500.06, 18421.42, 18178.8, 17880.6, 16040.75, 15391.02, 15253.75, 14619.0]
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
      categories: ['Ernst Handel', 'Mère Paillarde', 'Save-a-lot Markets', 'Rattlesnake Canyon Grocery', 'QUICK-Stop', 'Queen Cozinha', 'Piccolo und mehr', 'Hungry Owl All-Night Grocers', 'Blondel père et fils', 'Simons bistro'],
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
          text: "Total Revenue (USD)"
        }
    
    }
    };

    return (
    
      <div className={styles.graphContainer}>
        <div>
          <h1 style={{ textAlign: 'center',fontSize:'30px' }}>Top Customers by Revenue</h1>
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

  