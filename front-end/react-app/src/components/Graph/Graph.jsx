
    
import { useState,useEffect  } from "react";
import 'bootstrap/dist/css/bootstrap.min.css';
import styles from "./Graph.module.css";
import Carousel from 'react-bootstrap/Carousel';
import Arrow from '/teamspace/studios/this_studio/conv_analytics/front-end/react-app/public/arrow.svg';
import BarChart from './BarChart'
import LineChart from './LineChart'
import BarLineChart from './BarLineChart'
import PieChart from './PieChart'
import ScatterChart from './ScatterChart'
import Graph_0 from './Graph_0.jsx'

export function Graph({isGraph}) {
        const [data, setData] = useState(null);
        const [dataArray, setDataArray] = useState([]);
        const [loading, setLoading] = useState(false);
        const [error, setError] = useState(null);

        // Function to fetch data from your API endpoint
        const fetchData = async () => {
          setLoading(true);
          setError(null);
          
          try {
            const response = await fetch('/api/data');
            
            if (!response.ok) {
              const errorData = await response.json();
              throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }
            
            const jsonData = await response.json();
            setData(jsonData);
            
            // Convert to array if it's an object, or keep as array if it's already an array
            if (Array.isArray(jsonData)) {
              setDataArray(jsonData);
            } else if (typeof jsonData === 'object' && jsonData !== null) {
              // If it's an object, convert to array of key-value pairs or values
              setDataArray(Object.values(jsonData));
            } else {
              // If it's a primitive value, wrap in array
              setDataArray([jsonData]);
            }
            
          } catch (err) {
            setError(err.message);
            setData(null);
            setDataArray([]);
          } finally {
            setLoading(false);
          }
        };

        // Fetch data on component mount
        useEffect(() => {
          fetchData();
        }, []);

        const renderChart = (item) => {
          switch (item.type) {
            case 'bar':
              return <BarChart title={item.title} y_axis_title={item.y_axis_title} num_element={item.num_element} category_element={item.category_element} />;
            case 'line':
              return <LineChart title={item.title} y_axis_title={item.y_axis_title} num_element={item.num_element} category_element={item.category_element} />;
            case 'barline':
              return <BarLineChart title={item.title} y_bar_axis_title={item.y_bar_axis_title} y_line_axis_title={item.y_line_axis_title} num_element_bar={item.num_element_bar} num_element_line={item.num_element_line} category_element={item.category_element}/>;
            case 'pie':
              return <PieChart title={item.title} num_element={item.num_element} category_element={item.category_element} />;
            case 'scatter':
              return <ScatterChart title={item.title} output_string={item.y_axis_title} y_axis={item.y_axis} x_axis={item.x_axis}/>;
            default:
              return <Graph_0/>; // Default fallback
          }
        }

      return (
        isGraph ? (
        
            <div>         
              <Carousel 
                indicators={false} 
                interval={null}         
                prevIcon={<img className={styles.customPrevIcon} src={Arrow} alt="" />}       
                nextIcon={<img className={styles.customNextIcon} src={Arrow} alt="" />}       
              >         
                  {dataArray.length > 0 ? (

                      dataArray.map((item, index) => (
                        <Carousel.Item key={index}>
                          <div className={styles.graphContainer}>
                            {renderChart(item)}
                          </div>
                        </Carousel.Item>
                      ))
                ) : (
                    <Carousel.Item>
                      <div className={styles.graphContainer}>
                        <div>No data available</div>
                      </div>
                    </Carousel.Item>
                )}

              </Carousel>       
            </div>

        )
          : (
          <div className={styles.graphContainer}>
            <img className={styles.graph} src="/visual-data.png" alt="AI Chatbot Logo" />
          </div>
        )
      )
  
  }
    