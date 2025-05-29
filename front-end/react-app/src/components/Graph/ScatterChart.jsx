import { useState } from "react";
import Chart from "react-apexcharts";
import styles from "./Graph.module.css";
import Slider from "@mui/material/Slider";
import Box from "@mui/material/Box";

export default function ScatterChart({
  title,
  output_string,
  y_axis,
  x_axis,
  filter_added,
}) {
  function valuetext(value) {
    return `${value}`;
  }
  const [data, setData] = useState(initialData);
  const [dataVisual, setDataVisual] = useState(initialData);
  const [dataCategoryVisual, setDataCategoryVisual] = useState(
    initialData.map((item) => item.name)
  );
  const [value1, setValue1] = useState([
    Math.min(...initialData.map((item) => item.data[0][0])),
    Math.max(...initialData.map((item) => item.data[0][0])),
  ]);
  const [value2, setValue2] = useState([
    Math.min(...initialData.map((item) => item.data[0][1])),
    Math.max(...initialData.map((item) => item.data[0][1])),
  ]);

  const handleChangeSlicer1 = (event, newValue) => {
    setValue1(newValue);
    filterData(newValue, value2);
  };

  const handleChangeSlicer2 = (event, newValue) => {
    setValue2(newValue);
    filterData(value1, newValue);
  };

  const filterData = (range1, range2) => {
    const filteredData = initialData.filter((item) => {
      // Use initialData for filtering
      const firstValue = item.data[0][0];
      const secondValue = item.data[0][1];
      return (
        firstValue >= range1[0] &&
        firstValue <= range1[1] &&
        secondValue >= range2[0] &&
        secondValue <= range2[1]
      );
    });
    setDataVisual(filteredData);
    const uniqueCategories = [
      ...new Set(filteredData.map((item) => item.name)),
    ];
    setDataCategoryVisual(uniqueCategories);
  };

  const chartData = dataVisual.map((item) => ({
    name: item.name,
    data: item.data,
  }));

  var options = {
    colors: [
      "#1f77b4",
      "#ff7f0e",
      "#2ca02c",
      "#d62728",
      "#9467bd",
      "#8c564b",
      "#e377c2",
      "#7f7f7f",
      "#bcbd22",
      "#17becf",
    ],
    series: chartData,
    chart: {
      height: 350,
      type: "scatter",
      zoom: {
        enabled: true,
        type: "xy",
      },
    },
    xaxis: {
      tickAmount: 10,
      labels: {
        formatter: function (val) {
          return parseFloat(val).toFixed(1);
        },
      },
      title: {
        text: x_axis,
      },
    },
    yaxis: {
      labels: {
        formatter: function (val) {
          return parseFloat(val).toFixed(1);
        },
      },
      tickAmount: 7,
      title: {
        text: y_axis,
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
          type="scatter"
          width="220%"
          height="95%"
          series={options.series}
          options={options}
          align="center"
        ></Chart>
      </div>
      {filter_added && (
        <div>
          <div className={styles.filterContainer}>
            <Box sx={{ width: "25vw" }}>
              <Slider
                getAriaLabel={() => "{x_axis}"} // More descriptive label
                value={value1}
                onChange={handleChangeSlicer1}
                valueLabelDisplay="auto"
                getAriaValueText={valuetext}
                min={Math.min(...initialData.map((item) => item.data[0][0]))} // Use initialData for min/max
                max={Math.max(...initialData.map((item) => item.data[0][0]))} // Use initialData for min/max
              />
            </Box>
            <h4>{x_axis}</h4>
          </div>
          <div className={styles.filterContainer}>
            <Box sx={{ width: "25vw" }}>
              <Slider
                getAriaLabel={() => "{y_axis}"} // More descriptive label
                value={value2}
                onChange={handleChangeSlicer2}
                valueLabelDisplay="auto"
                getAriaValueText={valuetext}
                min={Math.min(...initialData.map((item) => item.data[0][1]))} // Use initialData for min/max
                max={Math.max(...initialData.map((item) => item.data[0][1]))} // Use initialData for min/max
              />
            </Box>
            <h4>{y_axis}</h4>
          </div>
        </div>
      )}
    </div>
  );
}
