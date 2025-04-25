
counter_path ="/teamspace/studios/this_studio/conv_analytics/config/counter.txt"

def update_counter():
    with open(counter_path, 'r', encoding='utf-8') as file:
      content = file.read()
    
    counter = int(content) + 1

    with open(counter_path, 'w') as file:
      file.write(str(counter))

def reset_counter():
  with open(counter_path, 'w') as file:
    file.write(str(0))

def get_counter():
  with open(counter_path, 'r', encoding='utf-8') as file:
      content = file.read()
    
  return int(content)

