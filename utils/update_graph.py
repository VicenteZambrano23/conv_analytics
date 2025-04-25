from utils.update_counter import get_counter

def update_graph():

    counter = get_counter()
    code = f"""
    
    import React, {{ useState }} from "react";
  import {{ Graph_{counter} }} from "./Graph_{counter}";

  export function Graph() {{
    
    return (<Graph_{counter}/>)
  
  }}
    """
    with open('/teamspace/studios/this_studio/conv_analytics/front-end/react-app/src/components/Graph/Graph.jsx', 'w') as file:
      file.write(code)