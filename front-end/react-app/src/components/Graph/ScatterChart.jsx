import { useState, useMemo } from "react";
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
  // Parse initial data with error handling
  const initialData = useMemo(() => {
    try {
      if (typeof output_string === 'string') {
        return JSON.parse(output_string);
      } else if (Array.isArray(output_string)) {
        return output_string;
      } else {
        console.error('Invalid output_string format');
        return [];
      }
    } catch (error) {
      console.error('Error parsing output_string:', error);
      return [];
    }
  }, [output_string]);

  function valuetext(value) {
    return `${value}`;
  }

  // Helper function to get min/max values safely
  const getMinMaxValues = (dataArray, index) => {
    if (!Array.isArray(dataArray) || dataArray.length === 0) {
      return [0, 100];
    }

    const values = [];
    dataArray.forEach(item => {
      if (item && item.data && Array.isArray(item.data)) {
        item.data.forEach(point => {
          if (Array.isArray(point) && point.length > index && typeof point[index] === 'number') {
            values.push(point[index]);
          }
        });
      }
    });
    
    if (values.length === 0) {
      return [0, 100];
    }
    
    const min = Math.min(...values);
    const max = Math.max(...values);
    
    // Ensure min and max are different to avoid slider issues
    if (min === max) {
      return [min - 1, max + 1];
    }
    
    return [min, max];
  };

  const [data, setData] = useState(initialData);
  const [dataVisual, setDataVisual] = useState(initialData);
  const [dataCategoryVisual, setDataCategoryVisual] = useState(
    initialData.map((item) => item.name || 'Unknown')
  );
  
  const [value1, setValue1] = useState(() => getMinMaxValues(initialData, 0));
  const [value2, setValue2] = useState(() => getMinMaxValues(initialData, 1));

  const handleChangeSlicer1 = (event, newValue) => {
    if (Array.isArray(newValue) && newValue.length === 2) {
      setValue1(newValue);
      filterData(newValue, value2);
    }
  };

  const handleChangeSlicer2 = (event, newValue) => {
    if (Array.isArray(newValue) && newValue.length === 2) {
      setValue2(newValue);
      filterData(value1, newValue);
    }
  };

  const filterData = (range1, range2) => {
    if (!Array.isArray(initialData)) {
      return;
    }

    const filteredData = initialData.map((item) => {
      if (!item || !item.data || !Array.isArray(item.data)) {
        return { ...item, data: [] };
      }

      // Filter individual points within each series
      const filteredPoints = item.data.filter(point => {
        if (!Array.isArray(point) || point.length < 2) {
          return false;
        }
        
        const firstValue = point[0];
        const secondValue = point[1];
        
        return (
          typeof firstValue === 'number' &&
          typeof secondValue === 'number' &&
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
    }).filter(item => item.data && item.data.length > 0); // Only keep series that have at least one point
    
    setDataVisual(filteredData);
    setData(filteredData); // Update the data state as well
    
    const uniqueCategories = [
      ...new Set(filteredData.map((item) => item.name || 'Unknown')),
    ];
    setDataCategoryVisual(uniqueCategories);
  };

  // Prepare chart data with safety checks
  const chartData = useMemo(() => {
    if (!Array.isArray(dataVisual)) {
      return [];
    }
    
    return dataVisual.map((item) => ({
      name: item.name || 'Unknown',
      data: Array.isArray(item.data) ? item.data : [],
    }));
  }, [dataVisual]);

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
        text: x_axis || 'X Axis',
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
        text: y_axis || 'Y Axis',
      },
    },
  };

  // Get min/max values for sliders safely
  const [minX, maxX] = getMinMaxValues(initialData, 0);
  const [minY, maxY] = getMinMaxValues(initialData, 1);

  // Don't render if no valid data
  if (!Array.isArray(initialData) || initialData.length === 0) {
    return (
      <div className={styles.graphContainer}>
        <div>
          <h1 style={{ textAlign: "center", fontSize: "30px" }}>
            {title || 'Scatter Chart'}
          </h1>
        </div>
        <div style={{ textAlign: 'center', padding: '50px' }}>
          <p>No data available to display</p>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.graphContainer}>
      <div>
        <h1 style={{ textAlign: "center", fontSize: "30px" }}>
          {title || 'Scatter Chart'}
        </h1>
      </div>
      <div className={styles.graphSubContainer}>
        <Chart
          type="scatter"
          width="220%"
          height="95%"
          series={chartData}
          options={options}
          align="center"
        />
      </div>
      {filter_added && (
        <div>
          <div className={styles.filterContainer}>
            <Box sx={{ width: "25vw" }}>
              <Slider
                getAriaLabel={() => x_axis || 'X Axis'}
                value={value1}
                onChange={handleChangeSlicer1}
                valueLabelDisplay="auto"
                getAriaValueText={valuetext}
                min={minX}
                max={maxX}
              />
            </Box>
            <h4>{x_axis || 'X Axis'}</h4>
          </div>
          <div className={styles.filterContainer}>
            <Box sx={{ width: "25vw" }}>
              <Slider
                getAriaLabel={() => y_axis || 'Y Axis'}
                value={value2}
                onChange={handleChangeSlicer2}
                valueLabelDisplay="auto"
                getAriaValueText={valuetext}
                min={minY}
                max={maxY}
              />
            </Box>
            <h4>{y_axis || 'Y Axis'}</h4>
          </div>
        </div>
      )}
    </div>
  );
}