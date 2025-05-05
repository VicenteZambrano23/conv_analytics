
import React, { useState } from "react";
import Carousel from 'react-bootstrap/Carousel';

import 'bootstrap/dist/css/bootstrap.min.css';
import { Graph_0 } from "./Graph_0";

import { Graph_1 } from "./Graph_1";

export function Graph() {

  
  return (<div>
      <Carousel indicators = {false} interval = {null} data-bs-theme="dark">
      <Carousel.Item >
          <Graph_1/>
        </Carousel.Item>, 
      
        
      </Carousel>
    </div>)
  
  }
    