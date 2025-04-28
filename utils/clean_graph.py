from utils.update_counter import get_counter
import os

def graph_clean():

  count = int(get_counter())
  
  for i in range(1,count+1):
    path = f"/teamspace/studios/this_studio/conv_analytics/front-end/react-app/src/components/Graph/Graph_{str(i)}.jsx"
    os.remove(path)

  code = """
    
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
    """
  with open('/teamspace/studios/this_studio/conv_analytics/front-end/react-app/src/components/Graph/Graph.jsx', 'w') as file:
      file.write(code)