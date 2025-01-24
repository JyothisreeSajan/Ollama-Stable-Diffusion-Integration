import requests
import io
from PIL import Image

def generate():
	API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-3.5-large"
	headers = {"Authorization": "Bearer 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"}

	def query(payload):
		response = requests.post(API_URL, headers=headers, json=payload)
		return response.content
	image_bytes = query({
		"inputs": " red moon and blue sun green sky",
	})

	# You can access the image with PIL.Image for example

	image = Image.open(io.BytesIO(image_bytes))
	image.show()
		
generate()