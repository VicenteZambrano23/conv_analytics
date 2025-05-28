import React, {useState } from "react";
import Chart from 'react-apexcharts';
import styles from "./Graph.module.css";


export default function BarLineChart({title,y_bar_axis_title,y_line_axis_title,num_element_bar,num_element_line, category_element}) {
  var options = {
        series: [{
        name: y_bar_axis_title,
        type: 'column',
        data: num_element_bar
      }, {
        name: y_line_axis_title,
        type: 'line',
        data: num_element_line,
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
        enabledOnSeries: [1],
        formatter: function (val) {
          return val.toFixed(0);
        },
      },
      labels: category_element,
      yaxis: [{
        title: {
          text: y_bar_axis_title,
        },
        labels: {
          formatter: function (val) {
            return val.toFixed(0);
          
        }
      }}, {
        opposite: true,
        title: {
          text: y_line_axis_title,
        },
        labels: {
          formatter: function (val) {
            return val.toFixed(0);
          }
        }
      }]
      };

  return (
        <div className={styles.graphContainer}>
            <div>
                <h1 style={{ textAlign: 'center',fontSize:'30px' }}>{title}</h1>
            </div>
            <div className={styles.graphSubContainer}>
                <Chart
                type='bar'
                width='220%'
                height='95%'
                series={options.series}
                options={options}
                align= 'center'
            ></Chart>
            </div>
        </div>
        )
}