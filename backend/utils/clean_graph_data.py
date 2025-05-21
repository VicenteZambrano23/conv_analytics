import os

graph_data_path = os.path.join(os.path.dirname(__file__), '..', 'database/graph_data.json')


def clean_graph_data():
    """
    Removes all content from the JSON file at the given path.
    If the file doesn't exist, it will be created (empty).

    Args:
        file_path (str): The full path to the JSON file.
    """
    try:
        with open(graph_data_path, 'w') as f:
            f.truncate(0)  # Truncate the file to 0 bytes, effectively clearing it
        print(f"Successfully cleared the content of: {graph_data_path}")
    except Exception as e:
        print(f"Error clearing the file {graph_data_path}: {e}")


clean_graph_data()