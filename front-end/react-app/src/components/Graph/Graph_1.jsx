
  import React, { useState } from "react";
 import Chart from 'react-apexcharts';
import styles from "./Graph.module.css";

 export function Graph_1() {
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
    <div className={styles.graphContainer}>
      <div>
        <h1 style={{ textAlign: 'center',fontSize:'30px' }}>Monthly Revenue Trend</h1>
      </div>
      <div  className={styles.graphSubContainer}>
        <Chart
        type= 'line'
        width='220%'
        height='95%' 
        series={options.series}
        options={options}
        align= 'center'
        ></Chart>
      </div>
    </div>)
 }

  