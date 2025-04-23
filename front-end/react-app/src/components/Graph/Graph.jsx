
  import React, { useState } from "react";
import Chart from 'react-apexcharts';

 export function Graph() {
 var options = {
  colors: ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"],
  series: [29, 25, 19, 18, 13, 12, 9, 9, 9, 8],
  
labels:['USA', 'Germany', 'Brazil', 'France', 'Austria', 'UK', 'Venezuela', 'Mexico', 'Canada', 'Finland'],
responsive: [{
  breakpoint: 480,
  options: {
    chart: {
      width: 200
    },
    legend: {
      position: 'bottom'
    }
  }
}],
dataLabels: {
  enabled: true,
  formatter: function (val) {
    return val.toFixed(1) + "%";
  },
  style: {
    colors: ['#fff'] // Set the text color to white
  },
  dropShadow: {
    enabled: true,
    top: 1,
    left: 1,
    blur: 2,
    color: '#000',
    opacity: 0.4
  }
},

    stroke: {
      width: 2, // Adjust the width of the separation line (in pixels)
      color: '#000' // Set the color of the separation line (e.g., white)
    },
};

 return (
<div style={{ textAlign: 'center' }}>
 <h1 style={{ textAlign: 'center' }}>Proportion of Orders by Country</h1>
 <Chart
 type= 'pie'
width={800} // Adjusted width to match your options
 height={500} // Adjusted height to match your options
 series={options.series}
 options={options}
 align= 'center'
 ></Chart></div>)
 }

  