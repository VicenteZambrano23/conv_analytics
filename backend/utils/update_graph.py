from utils.update_counter import get_counter
import os

graph_path = os.path.join(
    os.path.dirname(__file__), "..", "..", "front-end/react-app/src/components/Graph"
)


def update_graph():

    counter = int(get_counter() + 1)
    new_graph_str = ""
    second_graph_str = ""

    for i in range(1, counter + 1):

        new_graph_str += f"""
import {{ Graph_{i} }} from "./Graph_{i}";"""

        second_graph_str = (
            f"""
    <Carousel.Item >
      <div className={{styles.graphContainer}}>
        <Graph_{i}/>
      </div>
    </Carousel.Item> """
            + second_graph_str
        )

    code = f"""
import React, {{ useState }} from "react";
import Carousel from 'react-bootstrap/Carousel';
import styles from "./Graph.module.css";
import Arrow from '/teamspace/studios/this_studio/conv_analytics/front-end/react-app/public/arrow.svg';
import 'bootstrap/dist/css/bootstrap.min.css';
{new_graph_str}

export function Graph() {{

  
  return (<div>
      <Carousel indicators = {{false}} interval = {{null}}
      prevIcon = {{<img className={{styles.customPrevIcon}} src={{Arrow}} alt="" />}} 
    nextIcon = {{<img className={{styles.customNextIcon}} src={{Arrow}} alt="" />}}>
      {second_graph_str}
      
        
      </Carousel>
    </div>)
  
  }}
    """
    with open(os.path.join(graph_path, "/Graph.jsx"), "w") as file:
        file.write(code)
