import os
import json


path = os.path.join(os.path.dirname(__file__), "..", "database/graph_data.json.pdf")


def get_graph_data(key_number):
    """
    Retrieves the content from a JSON file based on the provided number key.

    Args:
        file_path (str): The full path to the JSON file.
        key_number (int): The integer key to search for in the JSON data.

    Returns:
        dict or None: The dictionary associated with the key if found,
                     otherwise None.
    """
    try:
        if os.path.exists(path):
            with open(path, "r") as f:
                data = json.load(f)
                key_str = str(key_number)  # Keys in JSON are strings
                if key_str in data:
                    return data[key_str]
                else:
                    print(f"Key '{key_number}' not found in the JSON data.")
                    return None
        else:
            print(f"File not found at: {path}")
            return None
    except FileNotFoundError:
        print(f"File not found at: {path}")
        return None
    except json.JSONDecodeError:
        print(
            f"Error decoding JSON from file: {path}. The file might be empty or corrupted."
        )
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
