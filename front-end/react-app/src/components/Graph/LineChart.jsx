import React, { useState } from "react";
import Chart from 'react-apexcharts';
import styles from "./Graph.module.css";

export default function LineChart({title, x_axis_title, y_axis_title,num_element,category_element}) {
        var options = {
            series: [{
            name: y_axis_title,
            data: num_element
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
            categories: category_element,
            title: {
            text: x_axis_title
            }
            },
            yaxis :{
            title :{
            text: y_axis_title
            }
            }
            };

        return (
        <div className={styles.graphContainer}>
            <div>
                <h1 style={{ textAlign: 'center',fontSize:'30px' }}>{title}</h1>
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
