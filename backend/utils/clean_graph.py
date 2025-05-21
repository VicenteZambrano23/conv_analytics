from utils.update_counter import get_counter
import os

graph_path  = os.path.join(os.path.dirname(__file__), '..','..', 'front-end/react-app/src/components/Graph')

def graph_clean():

  count = int(get_counter())
  
  for i in range(1,count+1):
    path = os.path.join(graph_path,f"/Graph_{str(i)}.jsx")
    os.remove(path)

  code = """
    
  import React, { useState } from "react";
  import 'bootstrap/dist/css/bootstrap.min.css';

import { Graph_0 } from "./Graph_0";

export function Graph() {

  
  return (<Graph_0/>)
  
  }
    """
  with open(os.path.join(graph_path,'/Graph.jsx'), 'w') as file:
      file.write(code)