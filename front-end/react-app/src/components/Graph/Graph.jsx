
import React, { useState } from "react";
import Carousel from 'react-bootstrap/Carousel';

import 'bootstrap/dist/css/bootstrap.min.css';
import { Graph_0 } from "./Graph_0";

import { Graph_1 } from "./Graph_1";
import { Graph_2 } from "./Graph_2";

export function Graph() {

  
  return (<div>
      <Carousel indicators = {false} interval = {null} data-bs-theme="dark">
      <Carousel.Item >
          <Graph_2/>
        </Carousel.Item>, <Carousel.Item >
          <Graph_1/>
        </Carousel.Item>, 
      
        
      </Carousel>
    </div>)
  
  }
    