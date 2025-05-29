import json
import os

json_path = os.path.join(os.path.dirname(__file__), '..', 'database/graph_data.json')

def update_json_fields( element_key, field_name, new_value, save_changes=True):
    """
    Update a specific field of an element in a JSON file.
    
    Args:
        file_path (str): Path to the JSON file
        element_key (str): The key of the element to update (e.g., "1")
        field_name (str): The name of the field to update (e.g., "title", "type", etc.)
        new_value: The new value to set for the field
        save_changes (bool): Whether to save changes back to the file (default: True)
    
    Returns:
        dict: The updated JSON data
        
    Raises:
        FileNotFoundError: If the JSON file doesn't exist
        JSONDecodeError: If the file contains invalid JSON
        KeyError: If element_key doesn't exist in the JSON data
    """
    # Check if file exists
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"JSON file not found: {json_path}")
    
    # Read the JSON file
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON in file {json_path}: {str(e)}")
    
    # Validate the structure
    if not isinstance(json_data, dict):
        raise TypeError("JSON file must contain a dictionary at root level")
    
    if element_key not in json_data:
        raise KeyError(f"Element key '{element_key}' not found in JSON data")
    
    # Update the field
    json_data[element_key][field_name] = new_value
    
    # Save changes back to file if requested
    if save_changes:
        with open(json_path, 'w', encoding='utf-8') as file:
            json.dump(json_data, file, indent=4, ensure_ascii=False)
    
    return json_data