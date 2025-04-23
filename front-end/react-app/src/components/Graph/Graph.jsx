
  import React, { useState } from "react";
  import Chart from 'react-apexcharts';

  export function Graph() {
    var options = {
      series: [{
      name: 'Total Sales (in monetary units)',
      data: [67764.5, 37487.87, 37067.2, 33650, 19043.5, 17207.8, 16785.0, 14638.0, 14208.7, 13498.0]
      }],
      chart: {
      height: 350,
      type: 'bar',
      },
    plotOptions: {
      bar: {
        borderRadius: 10,
        dataLabels: {
          position: 'top', // top, center, bottom
        },
      }
    },
    
    
    xaxis: {
      categories: ['Aux joyeux ecclésiastiques', 'Plutzer Lebensmittelgroßmärkte AG', 'Pavlova, Ltd.', 'Gai pâturage', "Forêts d'érables", "G'day, Mate", 'Formaggi Fortini s.r.l.', 'Norske Meierier', 'Specialty Biscuits, Ltd.', 'Pasta Buttini s.r.l.'],
      position: 'bottom',
      axisBorder: {
        show: true
      },
      axisTicks: {
        show: false
      },
      crosshairs: {
        fill: {
          type: 'gradient',
          gradient: {
            colorFrom: '#D8E3F0',
            colorTo: '#BED1E6',
            stops: [0, 100],
            opacityFrom: 0.4,
            opacityTo: 0.5,
          }
        }
      },
      tooltip: {
        enabled: true,
      }
    },
    yaxis: {
      axisBorder: {
        show: true
      },
      axisTicks: {
        show: true,
      },
      labels: {
        show: true,
        formatter: function (val) {
          return val;
        }
      },
      title: {
          text: 'Total Sales (in monetary units)'
        }
    
    }
    };

    return (
      <div style={{ textAlign: 'center' }}>
      <h1 style={{ textAlign: 'center' }}>Top 10 Suppliers by Total Sales</h1>
      <Chart
      type='bar'
      width={800} // Adjusted width to match your options
      height={500} // Adjusted height to match your options
      series={options.series}
      options={options}
      align= 'center'
  ></Chart></div>)
  }

  