
    
  import React, { useState } from "react";
import { Graph_0 } from "./Graph_0";

export function Graph() {

  const components = [<Graph_0 />];
  const [currentIndex, setCurrentIndex] = useState(0);

  const goToPrevious = () => {
    setCurrentIndex((prevIndex) => (prevIndex > 0 ? prevIndex - 1 : components.length - 1));
  };

  const goToNext = () => {
    setCurrentIndex((prevIndex) => (prevIndex < components.length - 1 ? prevIndex + 1 : 0));
  };
  return (<Graph_0/>)
  
  }
    