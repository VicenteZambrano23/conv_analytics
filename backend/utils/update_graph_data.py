import json
import os

graph_data_path = os.path.join(os.path.dirname(__file__), '..', 'database/graph_data.json')


def update_graph_data(data):

    existing_data = {}
    if os.path.exists(graph_data_path):
        try:
            with open(graph_data_path, "r") as f:
                existing_data = json.load(f)
        except json.JSONDecodeError:
            print("Warning: Existing JSON file is corrupted. Overwriting.")
            existing_data = {}

    existing_data.update(data)

    # Write the combined data back to the file
    try:
        with open(graph_data_path, "w") as f:
            json.dump(existing_data, f, indent=4)
        return f"JSON data appended to: {graph_data_path}"
    except Exception as e:
        return f"Error writing JSON to file: {e}"

