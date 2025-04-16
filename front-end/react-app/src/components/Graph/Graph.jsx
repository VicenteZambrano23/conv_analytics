import React, { useState } from "react";
import Chart from 'react-apexcharts';

export function Graph() {
  return (
    <Chart 
    type = 'bar'
    widht = {600}
    height={600}
    series={[{
      names: 'Company1',
      data :[100,200,232,132,422,122]
    },
    {
      names: 'Company2',
      data :[100,200,232,132,422,122]
    }
    ]
    }
    options={{
      colors:["#ff0000"]
    }}

    ></Chart>
  );
}



