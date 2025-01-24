import requests
import json

def run_ollama(prompt):
    url = "http://localhost:11434/api/chat"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": 'llama3.2',
        "messages": [{"role": "user", "content": prompt}],
        "stream": True  # Important to get streaming response
    }

    full_response = ""
    try:
        with requests.post(url, json=payload, headers=headers, stream=True) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    json_response = json.loads(decoded_line)
                    
                    if json_response.get('done'):
                        break
                    
                    if 'message' in json_response and json_response['message']['role'] == 'assistant':
                        chunk = json_response['message'].get('content', '')
                        full_response += chunk
                        print(chunk, end='', flush=True)
        
        return full_response
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

# Example Usage
if __name__ == "__main__":
    prompt = input("prompt: ")
    response = run_ollama(prompt)
    print("\nFull Ollama Response:", response)