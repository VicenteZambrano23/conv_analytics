
  import React, { useState } from "react";
  import Chart from 'react-apexcharts';
  import styles from "./Graph.module.css";
  
  export function Graph_1() {
    var options = {
      series: [{
      name: "Number of Orders",
      data: [10, 7, 7, 7, 6, 6, 5, 5, 5, 4]
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
      categories: ['Ernst Handel', 'Wartian Herkku', 'Rattlesnake Canyon Grocery', 'QUICK-Stop', 'Split Rail Beer & Ale', 'Hungry Owl All-Night Grocers', 'Mère Paillarde', "La maison d''Asie", 'LILA-Supermercado', 'Tortuga Restaurante'],
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
        </div>)
  }

  