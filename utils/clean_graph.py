from utils.update_counter import get_counter
import os

def graph_clean():

  count = int(get_counter())
  
  for i in range(1,count+1):
    path = f"/teamspace/studios/this_studio/conv_analytics/front-end/react-app/src/components/Graph/Graph_{str(i)}.jsx"
    os.remove(path)

  code = """
    
  import React, { useState } from "react";
  import 'bootstrap/dist/css/bootstrap.min.css';

import { Graph_0 } from "./Graph_0";

export function Graph() {

  
  return (<Graph_0/>)
  
  }
    """
  with open('/teamspace/studios/this_studio/conv_analytics/front-end/react-app/src/components/Graph/Graph.jsx', 'w') as file:
      file.write(code)