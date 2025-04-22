
import React, { useState } from "react";
import Chart from 'react-apexcharts';

export function Graph() {
var options = {
 series: [    {
          name: 'USA',
          data: [[69611.75, 29]]
    },
        {
          name: 'Austria',
          data: [[51671.96, 13]]
    },
        {
          name: 'Germany',
          data: [[47241.82, 25]]
    },
        {
          name: 'Brazil',
          data: [[40215.25, 19]]
    },
        {
          name: 'Canada',
          data: [[31326.35, 9]]
    },
        {
          name: 'France',
          data: [[29549.15, 18]]
    },
        {
          name: 'Denmark',
          data: [[17870.85, 4]]
    },
        {
          name: 'UK',
          data: [[16695.79, 12]]
    },
        {
          name: 'Ireland',
          data: [[15391.02, 6]]
    },
        {
          name: 'Venezuela',
          data: [[13556.28, 9]]
    },
        {
          name: 'Sweden',
          data: [[9720.8, 7]]
    },
        {
          name: 'Switzerland',
          data: [[8124.75, 4]]
    },
        {
          name: 'Belgium',
          data: [[8051.3, 2]]
    },
        {
          name: 'Finland',
          data: [[6438.5, 8]]
    },
        {
          name: 'Mexico',
          data: [[5861.56, 9]]
    },
        {
          name: 'Italy',
          data: [[4328.56, 7]]
    },
        {
          name: 'Spain',
          data: [[4302.19, 7]]
    },
        {
          name: 'Portugal',
          data: [[4170.0, 5]]
    },
        {
          name: 'Norway',
          data: [[1323.6, 1]]
    },
        {
          name: 'Poland',
          data: [[573.75, 1]]
    },
        {
          name: 'Argentina',
          data: [[399.0, 1]]
    },
    ],
 chart: {
 height: 350,
type: 'scatter',
zoom: {
 enabled: true,
type: 'xy'
 }
},
xaxis: {
 tickAmount: 10,
 labels: {
 formatter: function(val) {
 return parseFloat(val).toFixed(1)
 }
 },
 title: {
          text: 'Number of Orders'
        }
},
yaxis: {
tickAmount: 7,
title: {
          text: 'Total Revenue in USD'
        }
}
};

return (
<div style={{ textAlign: 'center' }}>
<h1 style={{ textAlign: 'center' }}>Scatter Plot of Revenue vs Number of Orders by Country</h1>
<Chart
type= 'scatter'
width={800} // Adjusted width to match your options
height={500} // Adjusted height to match your options
series={options.series}
options={options}
align= 'center'
></Chart></div>)
}

  