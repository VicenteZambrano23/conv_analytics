import os


jsx_code = "    hhh " 
with open(
          os.path.join(
    os.path.dirname(__file__), "..","..",f"front-end/src/components/Graph/Graph_{str(0+1)}.jsx"
),
            "w",
        ) as file:
            file.write(jsx_code)
