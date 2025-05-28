import { useState } from "react";
import Chart from 'react-apexcharts';
import styles from "./Graph.module.css";

export default function ScatterChart({title,output_string,y_axis,x_axis}) {
        var options = {
            colors: ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"],
            series: output_string,
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
                    text: x_axis
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
                    text: y_axis
                    }
            }
            };

        return (
            <div className={styles.graphContainer}>
                <div>
                    <h1 style={{ textAlign: 'center',fontSize:'30px' }}>{title}</h1>
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