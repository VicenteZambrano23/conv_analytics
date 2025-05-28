
    
  import React, { useState } from "react";
  import 'bootstrap/dist/css/bootstrap.min.css';
  import styles from "./Graph.module.css";
  import Carousel from 'react-bootstrap/Carousel';
  import Arrow from '/teamspace/studios/this_studio/conv_analytics/front-end/react-app/public/arrow.svg';

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
  return (
     isGraph ? (
     
        <div>         
          <Carousel 
            indicators={false} 
            interval={null}         
            prevIcon={<img className={styles.customPrevIcon} src={Arrow} alt="" />}       
            nextIcon={<img className={styles.customNextIcon} src={Arrow} alt="" />}       
          >         
            {second_graph_str}                             
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
    