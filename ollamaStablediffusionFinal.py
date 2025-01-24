import requests
import json
import io
from PIL import Image

def generate_image(prompt):
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-3.5-large"
    headers = {"Authorization": "Bearer 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"}

    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
        image_bytes = response.content
        
        image = Image.open(io.BytesIO(image_bytes))
        filename = "generated_image.png"
        image.show()
       # image.save(filename)
        return filename
    except Exception as e:
        return f"Image generation error: {e}"

def run_ollama(prompt):
    # Check if prompt suggests image generation
    image_keywords = ['create image','give image','give me an image','image','generate image', 'draw', 'make picture', 'illustrate']
    if any(keyword in prompt.lower() for keyword in image_keywords):
        
        for keyword in image_keywords:
            if keyword in prompt.lower():
                image_prompt = prompt.lower().split(keyword)[-1].strip()
                return generate_image(image_prompt)

    
    url = "http://localhost:11434/api/chat"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": 'llama3.2',
        "messages": [{"role": "user", "content": prompt}],
        "stream": True
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

if __name__ == "__main__":
    prompt = input("prompt: ")
    response = run_ollama(prompt)
    print("\nOllama Response:", response)