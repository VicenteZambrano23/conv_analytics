from utils.update_counter import get_counter

def update_graph():

  counter = int(get_counter())
  new_graph_str= ""
  second_graph_str = ""

  for i in range(1,counter+1):

    new_graph_str += f"""
      import {{ Graph_{i} }} from "./Graph_{i}";"""
    
    second_graph_str = f"""<Graph_{i}/>, """ + second_graph_str

  code = f"""
import React, {{ useState }} from "react";
import {{ Graph_0 }} from "./Graph_0";
{new_graph_str}

export function Graph() {{

  const components = [{second_graph_str} <Graph_0 />];
  const [currentIndex, setCurrentIndex] = useState(0);

  const goToPrevious = () => {{
    setCurrentIndex((prevIndex) => (prevIndex > 0 ? prevIndex - 1 : components.length - 1));
  }};

  const goToNext = () => {{
    setCurrentIndex((prevIndex) => (prevIndex < components.length - 1 ? prevIndex + 1 : 0));
  }};
  return (<div>
      <button onClick={{goToPrevious}}>&larr; Previous</button>
      <div>{{components[currentIndex]}}</div>
      <button onClick={{goToNext}}>Next &rarr;</button>
    </div>)
  
  }}
    """
  with open('/teamspace/studios/this_studio/conv_analytics/front-end/react-app/src/components/Graph/Graph.jsx', 'w') as file:
      file.write(code)

