
  import React, { useState } from "react";
  import Chart from 'react-apexcharts';

  export function Graph_1() {
    var options = {
      series: [{
      name: "Total Quantity Ordered",
      data: [1418, 839, 775, 573, 565, 553, 422, 367, 350, 321]
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
      categories: ['Ernst Handel', 'QUICK-Stop', 'Save-a-lot Markets', 'Rattlesnake Canyon Grocery', 'Hungry Owl All-Night Grocers', 'Frankenversand', 'Mère Paillarde', 'Blondel père et fils', 'Bottom-Dollar Marketse', 'Seven Seas Imports'],
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
          text: "Total Quantity Ordered"
        }
    
    }
    };

    return (
      <div style={{ textAlign: 'center' }}>
      <h1 style={{ textAlign: 'center',fontSize:'35px' }}>Top 10 Customers by Total Quantity Ordered</h1>
      <Chart
      type='bar'
      width={750} // Adjusted width to match your options
      height={475} // Adjusted height to match your options
      series={options.series}
      options={options}
      align= 'center'
  ></Chart></div>)
  }

  