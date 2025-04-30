
  import React, { useState } from "react";
  import Chart from 'react-apexcharts';

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
      <div style={{ textAlign: 'center' }}>
      <h1 style={{ textAlign: 'center',fontSize:'35px' }}>Top 10 Customers by Number of Orders</h1>
      <Chart
      type='bar'
      width={750} // Adjusted width to match your options
      height={475} // Adjusted height to match your options
      series={options.series}
      options={options}
      align= 'center'
  ></Chart></div>)
  }

  