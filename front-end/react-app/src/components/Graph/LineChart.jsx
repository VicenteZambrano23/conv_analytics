import React, { useState, useEffect } from "react";
import Chart from "react-apexcharts";
import styles from "./Graph.module.css";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

export default function LineChart({
  title,
  x_axis_title,
  y_axis_title,
  num_element,
  category_element,
  filter_added,
}) {
  // Original data and dates
  const originalData = num_element;
  const originalDates = category_element;

  // Convert string dates to Date objects for comparison
  const dateObjects = originalDates.map((dateStr) => {
    const [year, month] = dateStr.split("-");
    return new Date(parseInt(year), parseInt(month) - 1, 1);
  });

  // Get min and max dates from the dataset
  const minDate = new Date(Math.min(...dateObjects));
  const maxDate = new Date(Math.max(...dateObjects));

  // State for filtered data
  const [data, setData] = useState(originalData);
  const [dates, setDates] = useState(originalDates);

  // State for date pickers
  const [startDate, setStartDate] = useState(minDate);
  const [endDate, setEndDate] = useState(maxDate);

  // Filter data when date range changes
  useEffect(() => {
    filterDataByDateRange();
  }, [startDate, endDate]);

  // Function to handle start date change
  const handleStartDateChange = (date) => {
    setStartDate(date);
  };
  // Function to handle end date change
  const handleEndDateChange = (date) => {
    setEndDate(date);
  };
  // Function to filter data by date range
  const filterDataByDateRange = () => {
    const filteredIndexes = [];

    dateObjects.forEach((date, index) => {
      {
        if (date >= startDate && date <= endDate) {
          filteredIndexes.push(index);
        }
      }
    });

    const filteredData = filteredIndexes.map((index) => originalData[index]);
    const filteredDates = filteredIndexes.map((index) => originalDates[index]);

    setData(filteredData);
    setDates(filteredDates);
  };

  var options = {
    series: [
      {
        name: y_axis_title,
        data: data,
      },
    ],
    chart: {
      height: 350,
      type: "line",
      zoom: {
        enabled: false,
      },
    },
    dataLabels: {
      enabled: false,
    },
    stroke: {
      curve: "smooth",
      colors: ["#008FFB"],
    },

    grid: {
      row: {
        colors: ["#f3f3f3", "transparent"], // takes an array which will be repeated on columns
        opacity: 0.5,
      },
    },
    xaxis: {
      categories: dates,
      title: {
        text: x_axis_title,
      },
    },
    yaxis: {
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
          type="line"
          width="220%"
          height="95%"
          series={options.series}
          options={options}
          align="center"
        ></Chart>
      </div>
      {filter_added && (
        <div className={styles.dateContainer}>
          <DatePicker
            selected={startDate}
            onChange={handleStartDateChange}
            dateFormat="yyyy-MM"
            showMonthYearPicker
            placeholderText="Start Date"
          />
          <h4 style={{ marginLeft: "2vw", marginRight: "2vw" }}>to</h4>
          <DatePicker
            selected={endDate}
            onChange={handleEndDateChange}
            dateFormat="yyyy-MM"
            showMonthYearPicker
            placeholderText="End Date"
            minDate={startDate}
          />
        </div>
      )}
    </div>
  );
}
