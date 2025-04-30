
import React, { useState } from "react";
import Chart from 'react-apexcharts';

export function Graph_3() {
var options = {
  colors: ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"],
 series: [    {
          name: "Beverages",
          data: [[93, 35.365591397849464]]
    },
        {
          name: "Condiments",
          data: [[49, 22.887755102040817]]
    },
        {
          name: "Confections",
          data: [[84, 25.81238095238095]]
    },
        {
          name: "Dairy Products",
          data: [[100, 28.631999999999998]]
    },
        {
          name: "Grains/Cereals",
          data: [[42, 24.470238095238095]]
    },
        {
          name: "Meat/Poultry",
          data: [[50, 44.510200000000005]]
    },
        {
          name: "Produce",
          data: [[33, 33.03030303030303]]
    },
        {
          name: "Seafood",
          data: [[67, 20.07716417910448]]
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
          text: "Number of Orders"
        }
},
yaxis: {
  labels: {
    formatter: function(val) {
    return parseFloat(val).toFixed(1)
    }
    },
tickAmount: 7,
title: {
          text: "Average Price (USD)"
        }
}
};

return (
<div style={{ textAlign: 'center' }}>
<h1 style={{ textAlign: 'center', fontSize:'35px' }}>Number of Orders vs Average Price by Product Category</h1>
<Chart
type= 'scatter'
width={750} // Adjusted width to match your options
height={475} // Adjusted height to match your options
series={options.series}
options={options}
align= 'center'
></Chart></div>)
}

  