
  import React, { useState } from "react";
 import Chart from 'react-apexcharts';

 export function Graph_1() {
 var options = {
 series: [{
 name: "Total Order Value ($)",
data: []
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
categories: [],
title: {
  text: 'Month'
}
 },
 yaxis :{
  title :{
    text: "Total Order Value ($)"
  }
 }
 };

 return (
<div style={{ textAlign: 'center' }}>
 <h1 style={{ textAlign: 'center',fontSize:'35px' }}>Total Order Value Over the Last 6 Months</h1>
 <Chart
 type= 'line'
width={750} // Adjusted width to match your options
 height={475} // Adjusted height to match your options
 series={options.series}
 options={options}
 align= 'center'
 ></Chart></div>)
 }

  