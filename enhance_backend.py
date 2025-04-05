import os
import os.path as osp
import cv2
import numpy as np
import requests
import base64
from pathlib import Path
from io import BytesIO
from PIL import Image
from asset_converter import AssetConverter

# Create necessary directories
def ensure_directories():
    """Create all necessary directories for the application."""
    directories = ["temp", "output", "styles"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)

# Ensure directories exist
ensure_directories()

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def decode_base64_to_image(base64_string):
    image_data = base64.b64decode(base64_string)
    return Image.open(BytesIO(image_data))

def enhance_texture(file_path, denoising_strength=0.75, cfg_scale=7, steps=20, output_format=None):
    """
    Enhance a texture using Stable Diffusion and convert to desired format.
    
    Args:
        file_path: Path to the input file (PNG, DDS, or VTF)
        denoising_strength: Strength of the enhancement (0.0 to 1.0)
        cfg_scale: CFG scale for Stable Diffusion
        steps: Number of steps for Stable Diffusion
        output_format: Desired output format ('png', 'dds', or 'vtf')
        
    Returns:
        Path to the enhanced texture file
    """
    try:
        # Initialize asset converter
        converter = AssetConverter()
        
        # Determine input format and convert to PNG if needed
        input_format = os.path.splitext(file_path)[1].lower()
        original_format = None
        metadata_path = None
        
        if input_format in ['.dds', '.vtf']:
            print(f"Converting {input_format} to PNG...")
            png_path, metadata_path = converter.convert_to_png(file_path)
            if png_path is None:
                raise Exception(f"Failed to convert {input_format} to PNG")
            original_format = input_format[1:]  # Remove the dot
        else:
            png_path = file_path
        
        # Encode the image for API request
        with open(png_path, "rb") as f:
            encoded_image = base64.b64encode(f.read()).decode("utf-8")
        
        # Send request to Stable Diffusion API
        try:
            response = requests.post(
                "http://127.0.0.1:7860/sdapi/v1/img2img",
                json={
                    "init_images": [encoded_image],
                    "prompt": "",
                    "denoising_strength": denoising_strength,
                    "cfg_scale": cfg_scale,
                    "steps": steps
                },
                timeout=300  # 5-minute timeout
            )
            response.raise_for_status()  # Raise exception for bad status codes
        except requests.exceptions.ConnectionError:
            raise Exception("Could not connect to Stable Diffusion WebUI. Please ensure it's running on http://127.0.0.1:7860")
        except requests.exceptions.Timeout:
            raise Exception("Request to Stable Diffusion WebUI timed out. The model might be busy or the image too large.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error communicating with Stable Diffusion WebUI: {str(e)}")
        
        # Decode and save the enhanced image
        try:
            enhanced_image = base64.b64decode(response.json()["images"][0])
            enhanced_path = os.path.join("temp", "enhanced.png")
            with open(enhanced_path, "wb") as f:
                f.write(enhanced_image)
        except (KeyError, IndexError) as e:
            raise Exception(f"Invalid response from Stable Diffusion WebUI: {str(e)}")
        
        # Convert back to original format if specified
        if output_format:
            try:
                final_path = converter.convert_from_png(
                    enhanced_path,
                    output_format,
                    metadata_path=metadata_path
                )
                if final_path is None:
                    raise Exception(f"Failed to convert enhanced image to {output_format}")
            except Exception as e:
                print(f"Warning: Could not convert to {output_format}, saving as PNG instead: {str(e)}")
                final_path = enhanced_path
        else:
            final_path = enhanced_path
        
        return final_path
        
    except Exception as e:
        print(f"Error in enhance_texture: {str(e)}")
        raise