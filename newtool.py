import asyncio
import requests
import json
import io
import gradio as gr
from PIL import Image
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def generate_image(prompt):
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-3.5-large"
    headers = {"Authorization": "Bearer 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"}
    
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
        response.raise_for_status()
        
        image_bytes = response.content
        image = Image.open(io.BytesIO(image_bytes))
        
        # Generate filename with timestamp
        filename = f"generated_image_{datetime.now().strftime('%y%m%d_%H%M%S')}.png"
        
        return image
    except Exception as e:
        logger.error(f"Image generation error: {e}")
        return None

async def generate_text(prompt):
    API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-1B"
    headers = {"Authorization": "Bearer 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"}
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 250,  # Limit token generation
            "return_full_text": False  # Return only generated text
        }
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        
        # Handle list response
        output = response.json()
        
        # Extract text from the first item in the list
        if isinstance(output, list) and output:
            generated_text = output[0].get('generated_text', 'No response from Llama model.')
            return generated_text
        
        return "No valid response generated."
    
    except Exception as e:
        logger.error(f"Text generation error: {e}")
        return f"Text generation error: {e}"

async def run_ollama(prompt):
    # Extract the specific item to generate
    item = prompt.lower().replace("create image of", "").replace("give description", "").strip()
    
    # Create tasks for concurrent execution
    image_task = asyncio.create_task(generate_image(item))
    text_task = asyncio.create_task(generate_text(f"Write a creative and detailed description of a {item}. Include its visual characteristics, significance, and interesting details. Make the description vibrant and engaging."))
    
    # Await both tasks
    image = await image_task
    text = await text_task
    
    return text, image

def generate_response(prompt):
    text_response, image_response = asyncio.run(run_ollama(prompt))
    return text_response, image_response

# Create Gradio interface
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