import requests
import json
import sys
import time

def parse_and_print(json_data):
    """Parse and print relevant information from the JSON data."""
    if 'status' in json_data:
        print(f"Status: {json_data['status']}")
    
    if 'digest' in json_data:
        print(f"Digest: {json_data['digest']}")
    
    if 'total' in json_data:
        print(f"Total: {json_data['total']}")
    
    if 'completed' in json_data:
        print(f"Completed: {json_data['completed']}")

    print() 


def print_in_place(json_data):
    """Print relevant information from the JSON data in place."""
    status = json_data.get('status', 'Unknown status')
    digest = json_data.get('digest', '')
    total = json_data.get('total', '')
    completed = json_data.get('completed', '')

    # Build the output string
    output = f"Status: {status}"
    # if digest:
    #     output += f", Digest: {digest}"
    if total:
        output += f", Total: {total}"
    if completed:
        output += f", Completed: {completed}"
    # if total and completed:
    #     output += f", Percentage: {completed/total}"

    # Print in place
    print(output, end='\r')  # Overwrite the previous line
    sys.stdout.flush()  # Ensure the output is displayed immediately    
    time.sleep(0.5)  # Optional delay for visibility


def pull_model(model_name, stream=True):
    url = "http://localhost:11434/api/pull"  # Ollama server URL
    payload = {
        "name": model_name
    }

    try:
        # Make the POST request
        response = requests.post(url, json=payload, stream=stream)
        response.raise_for_status()  # Raise an error for bad responses

        if stream:
            print("Streaming response:")
            for line in response.iter_lines():
                if line:
                    data = line.decode('utf-8')
                    try:
                        json_data = json.loads(data)
                        print_in_place(json_data)
                        # print(json_data)  # Print each streamed JSON object
                    except json.JSONDecodeError:
                        print("Error decoding JSON:", data)
        else:
            # If not streaming, print the full response
            # print("Full Response:", response.json())
            parsed_response = response.json()
            print_in_place(parsed_response)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # model_name = "llama3.2:1b"  # Replace with the desired model name
    model_name = "nemotron-mini"  # Use quantized version if available
    model_name = "qwen2:1.5b"
    model_name = "deepseek-coder-v2:16b"

    pull_model(model_name, stream=True)  # Set stream to True or False as needed
    print()
