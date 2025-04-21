
def graph_clean():
    code = """
    
  import React, { useState } from "react";
  import Chart from 'react-apexcharts';

  export function Graph() {
    

    return (
      <div style={{ display: 'flex', justifyContent: 'center' ,textAlign: 'center'}}>
        <img  style = {{width: 400, height: 400,  justifyContent: 'center',display: 'block', // Or potentially 'inline-block' depending on context
    marginLeft: 'auto',
    marginRight: 'auto',
    marginTop: 100}} src="/visual-data.png" alt="AI Chatbot Logo" />
     </div>)
  }
    """
    with open('/teamspace/studios/this_studio/conv_analytics/front-end/react-app/src/components/Graph/Graph.jsx', 'w') as file:
      file.write(code)