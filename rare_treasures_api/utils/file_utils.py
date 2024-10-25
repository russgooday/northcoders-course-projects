''' Module for file operations '''
import json

def load_json_data(file_path: str) -> dict:
    '''Load JSON data from the file based on the provided key'''
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise RuntimeError(f'Error loading {file_path}: {e}') from e
