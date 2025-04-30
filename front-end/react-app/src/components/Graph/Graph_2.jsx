
  import React, { useState } from "react";
 import Chart from 'react-apexcharts';

 export function Graph_2() {
 var options = {
 series: [{
 name: "Revenue (USD)",
data: [37779.85, 33285.49, 34565.6, 51528.69, 62163.99, 63721.23, 83400.47, 19978.91]
 }],
 chart: {
 height: 350,
 type: 'line',
 zoom: {
 enabled: false
 }
  },
 dataLabels: {
enabled: false
 },
 stroke: {
curve: 'smooth',
colors: ['#008FFB']
 },

 grid: {
row: {
colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
 opacity: 0.5
},
 },
 xaxis: {
categories: ['1996-07', '1996-08', '1996-09', '1996-10', '1996-11', '1996-12', '1997-01', '1997-02'],
title: {
  text: 'Month'
}
 },
 yaxis :{
  title :{
    text: "Revenue (USD)"
  }
 }
 };

 return (
<div style={{ textAlign: 'center' }}>
 <h1 style={{ textAlign: 'center',fontSize:'35px' }}>Monthly Revenue Trend</h1>
 <Chart
 type= 'line'
width={750} // Adjusted width to match your options
 height={475} // Adjusted height to match your options
 series={options.series}
 options={options}
 align= 'center'
 ></Chart></div>)
 }

  