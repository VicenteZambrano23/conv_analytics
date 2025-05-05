
  import React, { useState } from "react";
  import Chart from 'react-apexcharts';

  export function Graph_1() {
    var options = {
          series: [{
          name: "Average Quantity",
          type: 'column',
          data: [28, 26, 25, 25, 24, 21, 21, 21]
        }, {
          name: "Average Price (USD)",
          type: 'line',
          data: [22, 28, 44, 25, 35, 24, 33, 20]
        }],
          chart: {
          height: 350,
          type: 'line',
        },
        stroke: {
          width: [0, 4]
        },
        markers: {
          shape: 'square',
          size: 12
        },
        dataLabels: {
          enabled: true,
          enabledOnSeries: [1]
        },
        labels: ['Condiments', 'Dairy Products', 'Meat/Poultry', 'Confections', 'Beverages', 'Grains/Cereals', 'Produce', 'Seafood'],
        yaxis: [{
          title: {
            text: "Average Quantity",
          },
        
        }, {
          opposite: true,
          title: {
            text: "Average Price (USD)",
          }
        }]
        };

    return (
      <div style={{ textAlign: 'center' }}>
      <h1 style={{ textAlign: 'center',fontSize:'35px' }}>Average Quantity and Price by Product Category</h1>
      <Chart
      type='bar'
      width={750} // Adjusted width to match your options
      height={475} // Adjusted height to match your options
      series={options.series}
      options={options}
      align= 'center'
  ></Chart></div>)
  }

  