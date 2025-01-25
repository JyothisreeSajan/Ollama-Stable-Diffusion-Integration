import asyncio
import requests
import json
import io
import gradio as gr
from PIL import Image
from datetime import datetime

async def generate_image(prompt):
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-3.5-large"
    headers = {"Authorization": "Bearer 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"}

    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
        response.raise_for_status()

        image_bytes = response.content
        image = Image.open(io.BytesIO(image_bytes))

        filename = f"generated_image_{datetime.now().strftime('%y%m%d_%H%M%S')}.png"
        image.save(filename)
        return image
    except Exception as e:
        return f"Image generation error: {e}"

async def run_ollama(prompt):
    # Extract the specific item to generate (e.g., "football")
    item = prompt.lower().replace("create image of", "").replace("give description", "").strip()
    
    # Concurrent tasks for image and text generation
    image_task = asyncio.create_task(generate_image(item))
    
    # Text generation
    url = "http://localhost:11434/api/chat"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": 'llama3.2',
        "messages": [
            {"role": "user", "content": f"Write a creative and detailed description of a {item}. Include its visual characteristics, significance, and interesting details. Make the description vibrant and engaging."}
        ],
        "stream": False  # Changed to False to get full response
    }

    try:
        # Send text generation request
        text_response = requests.post(url, json=payload, headers=headers).json()
        
        # Extract full text response
        full_response = text_response.get('message', {}).get('content', 'No description available.')
        
        # Wait for image generation
        image = await image_task
        
        return full_response, image
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}", None

def generate_response(prompt):
    text_response, image_response = asyncio.run(run_ollama(prompt))
    return text_response, image_response

iface = gr.Interface(
    fn=generate_response, 
    inputs=gr.Textbox(label="Enter your prompt", placeholder="Type here..."), 
    outputs=[
        gr.Textbox(label="Description"), 
        gr.Image(label="Generated Image", type="pil")
    ]
)

# Launch the Gradio app
iface.launch(share=True)

if __name__ == "__main__":
    prompt = input("prompt: ")
    text_response, image_response = asyncio.run(run_ollama(prompt))
    print("\nDescription:", text_response)