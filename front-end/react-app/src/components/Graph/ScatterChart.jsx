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
  const initialData = JSON.parse(output_string); // Fix: Parse the JSON string

  function valuetext(value) {
    return `${value}`;
  }

  const [data, setData] = useState(initialData);
  const [dataVisual, setDataVisual] = useState(initialData);
  const [dataCategoryVisual, setDataCategoryVisual] = useState(
    initialData.map((item) => item.name)
  );
  
  // Fix: Add safety checks for empty data
  const getMinMaxValues = (dataArray, index) => {
    const values = [];
    dataArray.forEach(item => {
      if (item.data && item.data.length > 0) {
        item.data.forEach(point => {
          if (point && point.length > index) {
            values.push(point[index]);
          }
        });
      }
    });
    return values.length > 0 ? [Math.min(...values), Math.max(...values)] : [0, 100];
  };

  const [value1, setValue1] = useState(() => getMinMaxValues(initialData, 0));
  const [value2, setValue2] = useState(() => getMinMaxValues(initialData, 1));

  const handleChangeSlicer1 = (event, newValue) => {
    setValue1(newValue);
    filterData(newValue, value2);
  };

  const handleChangeSlicer2 = (event, newValue) => {
    setValue2(newValue);
    filterData(value1, newValue);
  };

  const filterData = (range1, range2) => {
    const filteredData = initialData.map((item) => {
      // Filter individual points within each series
      const filteredPoints = item.data.filter(point => {
        const firstValue = point[0];
        const secondValue = point[1];
        return (
          firstValue >= range1[0] &&
          firstValue <= range1[1] &&
          secondValue >= range2[0] &&
          secondValue <= range2[1]
        );
      });
      
      return {
        ...item,
        data: filteredPoints
      };
    }).filter(item => item.data.length > 0); // Only keep series that have at least one point
    
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

  // Fix: Get min/max values for sliders safely
  const [minX, maxX] = getMinMaxValues(initialData, 0);
  const [minY, maxY] = getMinMaxValues(initialData, 1);

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
        />
      </div>
      {filter_added && (
        <div>
          <div className={styles.filterContainer}>
            <Box sx={{ width: "25vw" }}>
              <Slider
                getAriaLabel={() => x_axis} // Fix: Remove curly braces
                value={value1}
                onChange={handleChangeSlicer1}
                valueLabelDisplay="auto"
                getAriaValueText={valuetext}
                min={minX}
                max={maxX}
              />
            </Box>
            <h4>{x_axis}</h4>
          </div>
          <div className={styles.filterContainer}>
            <Box sx={{ width: "25vw" }}>
              <Slider
                getAriaLabel={() => y_axis} // Fix: Remove curly braces
                value={value2}
                onChange={handleChangeSlicer2}
                valueLabelDisplay="auto"
                getAriaValueText={valuetext}
                min={minY}
                max={maxY}
              />
            </Box>
            <h4>{y_axis}</h4>
          </div>
        </div>
      )}
    </div>
  );
}