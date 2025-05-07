
  import React, { useState } from "react";
  import Chart from 'react-apexcharts';
  import styles from "./Graph.module.css";

  export function Graph_3() {
    var options = {
          series: [{
          name: "Number of Orders",
          type: 'column',
          data: [59, 69, 57, 73, 66, 81, 85, 28]
        }, {
          name: "Revenue (USD)",
          type: 'line',
          data: [37779.85, 33285.49, 34565.6, 51528.69, 62163.99, 63721.23, 83400.47, 19978.91],
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
        labels: ['1996-07', '1996-08', '1996-09', '1996-10', '1996-11', '1996-12', '1997-01', '1997-02'],
        yaxis: [{
          title: {
            text: "Number of Orders",
          },
          labels: {
            formatter: function (val) {
              return val.toFixed(0);
            }
          }
        }, {
          opposite: true,
          title: {
            text: "Revenue (USD)",
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
          <h1 style={{ textAlign: 'center',fontSize:'30px' }}>Monthly Revenue and Number of Orders</h1>
        </div>
        <div className={styles.graphSubContainer}>
      <Chart
      type='bar'
      width='220%'
      height='95%'
      series={options.series}
      options={options}
      align= 'center'
  ></Chart></div>
  </div>)
  }

  