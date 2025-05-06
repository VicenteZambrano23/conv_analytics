
  import React, { useState } from "react";
import Chart from 'react-apexcharts';
import styles from "./Graph.module.css";

 export function Graph_1() {
 var options = {
  colors: ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"],
  series: [10, 7, 7, 7, 6, 6, 5, 5, 5, 4],
  
labels:['Ernst Handel', 'Wartian Herkku', 'Rattlesnake Canyon Grocery', 'QUICK-Stop', 'Split Rail Beer & Ale', 'Hungry Owl All-Night Grocers', 'Mère Paillarde', "La maison d''Asie", 'LILA-Supermercado', 'Tortuga Restaurante'],
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
    <div className={styles.graphContainer}>
      <div>
        <h1 style={{ textAlign: 'center',fontSize:'30px' }}>Top Customers by Number of Orders</h1>
      </div>
      <div className={styles.graphSubContainer}>
        <Chart
          type= 'pie'
          width='220%'
          height='95%' 
          series={options.series}
          options={options}
          align= 'center'
        ></Chart>
      </div>
    </div>)
 }

  