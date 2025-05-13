
import React, { useState } from "react";
import Carousel from 'react-bootstrap/Carousel';
import styles from "./Graph.module.css";
import Arrow from '/teamspace/studios/this_studio/conv_analytics/front-end/react-app/public/arrow.svg';
import 'bootstrap/dist/css/bootstrap.min.css';

import { Graph_1 } from "./Graph_1";
import { Graph_2 } from "./Graph_2";

export function Graph() {

  
  return (<div>
      <Carousel indicators = {false} interval = {null}
      prevIcon = {<img className={styles.customPrevIcon} src={Arrow} alt="" />} 
    nextIcon = {<img className={styles.customNextIcon} src={Arrow} alt="" />}>
      
    <Carousel.Item >
      <div className={styles.graphContainer}>
        <Graph_2/>
      </div>
    </Carousel.Item> 
    <Carousel.Item >
      <div className={styles.graphContainer}>
        <Graph_1/>
      </div>
    </Carousel.Item> 
      
        
      </Carousel>
    </div>)
  
  }
    