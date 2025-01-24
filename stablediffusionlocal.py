from diffusers import StableDiffusionPipeline
import torch

model_id = "stabilityai/stable-diffusion-xl-base-1.0"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
image = pipe("A pen on a white background").images[0]
image.save("generated_pen.png")