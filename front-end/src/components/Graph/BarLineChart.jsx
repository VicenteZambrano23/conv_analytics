import React, { useState, useEffect } from "react";
import Chart from "react-apexcharts";
import styles from "./Graph.module.css";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

export default function BarLineChart({
  title,
  y_bar_axis_title,
  y_line_axis_title,
  num_element_bar,
  num_element_line,
  category_element,
  filter_added,
}) {
  // Original data and dates
  const originalOrdersData = num_element_bar;
  const originalRevenueData = num_element_line;
  const originalLabels = category_element;

  // State for filtered data
  const [ordersData, setOrdersData] = useState(originalOrdersData);
  const [revenueData, setRevenueData] = useState(originalRevenueData);
  const [labels, setLabels] = useState(originalLabels);

  // Convert string dates to Date objects for comparison
  const dateObjects = originalLabels.map((dateStr) => {
    const [year, month] = dateStr.split("-");
    return new Date(parseInt(year), parseInt(month) - 1, 1);
  });

  // Get min and max dates from the dataset
  const minDate = new Date(Math.min(...dateObjects));
  const maxDate = new Date(Math.max(...dateObjects));

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
      if (date >= startDate && date <= endDate) {
        filteredIndexes.push(index);
      }
    });

    const filteredOrdersData = filteredIndexes.map(
      (index) => originalOrdersData[index]
    );
    const filteredRevenueData = filteredIndexes.map(
      (index) => originalRevenueData[index]
    );
    const filteredLabels = filteredIndexes.map(
      (index) => originalLabels[index]
    );

    setOrdersData(filteredOrdersData);
    setRevenueData(filteredRevenueData);
    setLabels(filteredLabels);
  };
  var options = {
    series: [
      {
        name: y_bar_axis_title,
        type: "column",
        data: num_element_bar,
      },
      {
        name: y_line_axis_title,
        type: "line",
        data: num_element_line,
      },
    ],
    chart: {
      height: 350,
      type: "line",
    },
    stroke: {
      width: [0, 4],
    },
    markers: {
      shape: "square",
      size: 12,
    },
    dataLabels: {
      enabled: true,
      enabledOnSeries: [1],
      formatter: function (val) {
        return val.toFixed(0);
      },
    },
    labels: category_element,
    yaxis: [
      {
        title: {
          text: y_bar_axis_title,
        },
        labels: {
          formatter: function (val) {
            return val.toFixed(0);
          },
        },
      },
      {
        opposite: true,
        title: {
          text: y_line_axis_title,
        },
        labels: {
          formatter: function (val) {
            return val.toFixed(0);
          },
        },
      },
    ],
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
