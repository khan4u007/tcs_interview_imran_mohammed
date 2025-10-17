import json
import requests

# Constants
EXAMPLE_JSON_FILE = "example.json"
API_URL = ""

def read_and_validate_json(filename):
    """Reads and validates JSON from a file."""
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        return data
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
        return None
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return None

def filter_non_private_objects(data):
    """Filters objects with 'private' set to False."""
    if isinstance(data, list):
        return [obj for obj in data if not obj.get("private", False)]
    elif isinstance(data, dict):
        return {k: v for k, v in data.items() if not v.get("private", False)}
    else:
        print("Unsupported JSON structure. Expected list or dict at root.")
        return None

def post_to_service(filtered_data):
    """Sends a POST request with filtered data to the service endpoint."""
    try:
        response = requests.post(API_URL, json=filtered_data, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"HTTP Request failed: {e}")
        return None
    except json.JSONDecodeError:
        print("Response was not valid JSON.")
        return None

def print_valid_keys(response_data):
    """Prints keys where 'valid' attribute is True."""
    if not isinstance(response_data, dict):
        print("Unexpected response format.")
        return

    for key, value in response_data.items():
        if isinstance(value, dict) and value.get("valid", False) is True:
            print(key)

def main():
    raw_data = read_and_validate_json(EXAMPLE_JSON_FILE)
    if raw_data is None:
        return

    filtered = filter_non_private_objects(raw_data)
    if filtered is None:
        return

    response = post_to_service(filtered)
    if response is None:
        return

    print_valid_keys(response)

if __name__ == "__main__":
    main()
