import React, { useState } from "react";
import Chart from "react-apexcharts";
import styles from "./Graph.module.css";
import Box from "@mui/material/Box";
import Slider from "@mui/material/Slider";

export default function BarChart({
  title,
  y_axis_title,
  num_element,
  category_element,
  filter_added

}) {
  function valuetext(value) {
    return `${value}`;
  }
  const data = num_element;
  const dataCategory = category_element;
  const [dataVisual, setDataVisual] = useState(data);
  const [dataCategoryVisual, setDataCategoryVisual] = useState(dataCategory);
  const [value, setValue] = useState([Math.min(...data), Math.max(...data)]);

  const handleChange = (event, newValue) => {
    const filteredData = data.filter(
      (item) => item >= Math.min(...newValue) && item <= Math.max(...newValue)
    );
    setDataVisual(filteredData);

    // Create a Set to store unique categories
    const uniqueCategories = new Set();

    // Iterate through the original data and categories
    data.forEach((item, index) => {
      if (item >= Math.min(...newValue) && item <= Math.max(...newValue)) {
        uniqueCategories.add(dataCategory[index]);
      }
    });

    setDataCategoryVisual(Array.from(uniqueCategories));
    setValue(newValue);
  };

  var options = {
    series: [
      {
        name: y_axis_title,
        data: dataVisual,
      },
    ],
    chart: {
      height: 350,
      type: "bar",
    },
    plotOptions: {
      bar: {
        borderRadius: 10,
        dataLabels: {
          position: "top", // top, center, bottom
        },
      },
    },

    xaxis: {
      categories: dataCategoryVisual,
      position: "bottom",
      axisBorder: {
        show: true,
      },
      axisTicks: {
        show: false,
      },
      crosshairs: {
        fill: {
          type: "gradient",
          gradient: {
            colorFrom: "#D8E3F0",
            colorTo: "#BED1E6",
            stops: [0, 100],
            opacityFrom: 0.4,
            opacityTo: 0.5,
          },
        },
      },
      tooltip: {
        enabled: true,
      },
    },
    yaxis: {
      axisBorder: {
        show: true,
      },
      axisTicks: {
        show: true,
      },
      labels: {
        show: true,
        formatter: function (val) {
          return val;
        },
      },
      title: {
        text: y_axis_title,
      },
    },
  };

  return (
    <div className={styles.graphContainer}>
      <div>
        <h1 style={{ textAlign: "center", fontSize: "30px" }}>{title}</h1>
      </div>
      <div className={styles.graphSubContainer}>
        <Chart
          type="bar"
          width="220%"
          height="95%"
          series={options.series}
          options={options}
          align="center"
        ></Chart>
      </div>
      {filter_added &&
      (<div className={styles.filterContainer}>
        <Box sx={{ width: "25vw" }}>
          <Slider
            getAriaLabel={() => "Range"}
            value={value}
            onChange={handleChange}
            valueLabelDisplay="auto"
            getAriaValueText={valuetext}
            min={Math.min(...data)}
            max={Math.max(...data)}
          />
        </Box>
      </div>)}
    </div>
  );
}
