from utils.update_counter import get_counter

def update_graph():

  counter = int(get_counter())
  new_graph_str= ""
  second_graph_str = ""

  for i in range(1,counter+1):

    new_graph_str += f"""
import {{ Graph_{i} }} from "./Graph_{i}";"""
    
    second_graph_str = f"""<Carousel.Item >
          <Graph_{i}/>
        </Carousel.Item>, """ + second_graph_str

  code = f"""
import React, {{ useState }} from "react";
import Carousel from 'react-bootstrap/Carousel';

import 'bootstrap/dist/css/bootstrap.min.css';
import {{ Graph_0 }} from "./Graph_0";
{new_graph_str}

export function Graph() {{

  
  return (<div>
      <Carousel indicators = {{false}} interval = {{null}} data-bs-theme="dark">
      {second_graph_str}
      
        
      </Carousel>
    </div>)
  
  }}
    """
  with open('/teamspace/studios/this_studio/conv_analytics/front-end/react-app/src/components/Graph/Graph.jsx', 'w') as file:
      file.write(code)

