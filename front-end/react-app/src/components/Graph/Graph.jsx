
  import React, { useState } from "react";
import Chart from 'react-apexcharts';

 export function Graph() {
 var options = {
  colors: ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"],
  series: [69611.75, 51671.96, 47241.82, 40215.25, 31326.35, 29549.15, 17870.85, 16695.79, 15391.02, 13556.28],
  
labels:['USA', 'Austria', 'Germany', 'Brazil', 'Canada', 'France', 'Denmark', 'UK', 'Ireland', 'Venezuela'],
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
 <h1 style={{ textAlign: 'center' }}>Top 10 Countries by Total Revenue</h1>
 <Chart
 type= 'pie'
width={800} // Adjusted width to match your options
 height={500} // Adjusted height to match your options
 series={options.series}
 options={options}
 align= 'center'
 ></Chart></div>)
 }

  