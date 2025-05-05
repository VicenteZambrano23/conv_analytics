
import React, { useState } from "react";
import Chart from 'react-apexcharts';
import styles from "./Graph.module.css";

export function Graph_3() {
var options = {
  colors: ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"],
 series: [    {
          name: "Beverages",
          data: [[18, 8], [19, 11], [4.5, 11], [14, 6], [18, 9], [263.5, 7], [18, 8], [46, 6], [14, 1], [15, 8], [7.75, 8], [18, 10]]
    },
        {
          name: "Condiments",
          data: [[10, 2], [22, 5], [21.35, 4], [25, 2], [40, 2], [15.5, 2], [19.45, 5], [28.5, 2], [43.9, 6], [21.05, 9], [17, 2], [13, 8]]
    },
        {
          name: "Produce",
          data: [[30, 2], [23.25, 8], [45.6, 10], [53, 6], [10, 7]]
    },
        {
          name: "Meat/Poultry",
          data: [[97, 1], [39, 11], [123.79, 9], [32.8, 10], [7.45, 12], [24, 7]]
    },
        {
          name: "Seafood",
          data: [[31, 4], [6, 7], [62.5, 5], [25.89, 8], [19, 9], [26, 3], [18.4, 8], [9.65, 9], [9.5, 1], [12, 7], [13.25, 4], [15, 2]]
    },
        {
          name: "Dairy Products",
          data: [[21, 9], [38, 2], [12.5, 14], [32, 3], [2.5, 9], [55, 14], [34, 12], [36, 10], [21.5, 13], [34.8, 14]]
    },
        {
          name: "Confections",
          data: [[17.45, 10], [9.2, 9], [81, 5], [10, 8], [14, 4], [31.23, 8], [43.9, 3], [9.5, 3], [12.75, 1], [20, 6], [16.25, 3], [49.3, 13], [12.5, 11]]
    },
        {
          name: "Grains/Cereals",
          data: [[21, 2], [9, 4], [14, 6], [7, 3], [38, 12], [19.5, 8], [33.25, 7]]
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
          text: "Product Price"
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
          text: "Number of Orders"
        }
}
};

return (
      <div className={styles.graphContainer}>
        <div>
          <h1 style={{ textAlign: 'center',fontSize:'30px' }}>Relationship between Number of Orders and Product Price by Category</h1>
        </div>
        <div className={styles.graphSubContainer}>
          <Chart
          type= 'scatter'
          width='220%'
          height='95%' 
          series={options.series}
          options={options}
          align= 'center'
          ></Chart>
        </div>
      </div>)
}

  