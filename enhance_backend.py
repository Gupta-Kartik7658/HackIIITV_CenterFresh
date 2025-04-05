import os.path as osp
import cv2
import numpy as np
import requests
import base64
from pathlib import Path
from io import BytesIO
from PIL import Image

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def decode_base64_to_image(base64_string):
    image_data = base64.b64decode(base64_string)
    return Image.open(BytesIO(image_data))

def enhance_texture(file_path, denoising_strength=0.75, cfg_scale=7, steps=30):
    # Prepare input
    input_dir = Path("LR")
    output_dir = Path("results")
    input_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)

    # Save uploaded file to LR folder
    base_name = osp.splitext(osp.basename(file_path))[0]
    lr_path = input_dir / f"{base_name}.png"
    img = cv2.imread(str(file_path), cv2.IMREAD_COLOR)
    cv2.imwrite(str(lr_path), img)

    # Encode image for API request
    encoded_image = encode_image_to_base64(lr_path)

    # Send request to Stable Diffusion API
    try:
        response = requests.post(
            "http://127.0.0.1:7860/sdapi/v1/img2img",
            json={
                "init_images": [encoded_image],
                "prompt": "semi-realistic pixel art remaster, detailed, high-res",
                "denoising_strength": denoising_strength,
                "cfg_scale": cfg_scale,
                "steps": steps
            }
        )
        
        if response.status_code == 200:
            # Decode and save the enhanced image
            result = response.json()
            enhanced_image = decode_base64_to_image(result['images'][0])
            enhanced_path = output_dir / f"{base_name}_enhanced.png"
            enhanced_image.save(enhanced_path)
            return enhanced_path
        else:
            raise Exception(f"API request failed with status code: {response.status_code}")
    except Exception as e:
        print(f"Error during enhancement: {str(e)}")
        return None