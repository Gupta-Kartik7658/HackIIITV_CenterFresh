import streamlit as st
from PIL import Image
from pathlib import Path
import os
import tempfile
import requests
import base64
import json
import imageio.v3 as iio
import numpy as np
import struct
from asset_converter import AssetConverter  # Assumed to be your DDS-to-PNG converter

# Ensure necessary directories exist
def ensure_directories():
    """Create required directories for temporary files."""
    directories = ["temp", "styles"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)

ensure_directories()

# Function to create DDS header (from your provided code)
def create_dds_header(width, height, fourcc):
    dwSize = 124
    dwFlags = 0x0002100F  # CAPS | HEIGHT | WIDTH | PIXELFORMAT | LINEARSIZE
    dwPitchOrLinearSize = width * 4  # Assuming RGBA8
    dwCaps = 0x1000  # CAPS_TEXTURE
    dwCaps2 = 0

    pfSize = 32
    pfFlags = 0x41  # DDPF_RGB | DDPF_ALPHAPIXELS
    pfFourCC = fourcc.encode('ascii')
    pfRGBBitCount = 32
    pfRBitMask = 0x00FF0000
    pfGBitMask = 0x0000FF00
    pfBBitMask = 0x000000FF
    pfABitMask = 0xFF000000

    header = b"DDS "
    header += struct.pack("<I", dwSize)
    header += struct.pack("<I", dwFlags)
    header += struct.pack("<I", height)
    header += struct.pack("<I", width)
    header += struct.pack("<I", dwPitchOrLinearSize)
    header += struct.pack("<I", 0)  # dwDepth
    header += struct.pack("<I", 0)  # dwMipMapCount
    header += b"\x00" * 44  # Reserved1

    # DDS_PIXELFORMAT (32 bytes)
    header += struct.pack("<I", pfSize)
    header += struct.pack("<I", pfFlags)
    header += pfFourCC.ljust(4, b'\x00')  # Pad FourCC to 4 bytes
    header += struct.pack("<I", pfRGBBitCount)
    header += struct.pack("<I", pfRBitMask)
    header += struct.pack("<I", pfGBitMask)
    header += struct.pack("<I", pfBBitMask)
    header += struct.pack("<I", pfABitMask)

    # Caps
    header += struct.pack("<I", dwCaps)
    header += struct.pack("<I", dwCaps2)
    header += b"\x00" * 12  # Caps3, Caps4, Reserved2

    return header

# Function to enhance texture and convert to desired format
def enhance_texture(file_path, prompt,negative_prompt ,denoising_strength=0.25, cfg_scale=4, steps=40, output_format=None, metadata_path=None):
    """
    Enhance a texture using Stable Diffusion and convert to the desired format.
    
    Args:
        file_path (str): Path to the input PNG file.
        prompt (str): Prompt for Stable Diffusion enhancement.
        denoising_strength (float): Strength of enhancement (0.0 to 1.0).
        cfg_scale (int): CFG scale for prompt adherence.
        steps (int): Number of diffusion steps.
        output_format (str): Desired output format ('png', 'dds', 'vtf').
        metadata_path (str, optional): Path to metadata for DDS conversion.
    
    Returns:
        str: Path to the enhanced texture file.
    """
    try:
        # Encode the input PNG for Stable Diffusion API
        with open(file_path, "rb") as f:
            encoded_image = base64.b64encode(f.read()).decode("utf-8")
        
        # Send request to Stable Diffusion API
        response = requests.post(
            "http://127.0.0.1:7860/sdapi/v1/img2img",
            json={
                "init_images": [encoded_image],
                "prompt": prompt,
                "negative_prompt": negative_prompt
                "denoising_strength": denoising_strength,
                "cfg_scale": cfg_scale,
                "steps": steps
            },
            timeout=300
        )
        response.raise_for_status()

        # Decode and save the enhanced image as PNG
        enhanced_image = base64.b64decode(response.json()["images"][0])
        enhanced_png_path = os.path.join("temp", "enhanced.png")
        with open(enhanced_png_path, "wb") as f:
            f.write(enhanced_image)

        # Convert to DDS if output_format is 'dds' and metadata is provided
        if output_format == 'dds' and metadata_path:
            try:
                # Load metadata
                with open(metadata_path, "r") as f:
                    metadata = json.load(f)
                
                # Get FourCC from metadata (default to DXT1 if not found)
                fourcc = metadata.get("fourcc", "DXT1")[:4]
                
                # Read the enhanced PNG
                image = iio.imread(enhanced_png_path)
                height, width = image.shape[:2]
                
                # Add alpha channel if image is RGB (3 channels)
                if image.shape[2] == 3:
                    image = np.dstack((image, np.full((height, width), 255, dtype=np.uint8)))
                
                # Convert to RGBA bytes
                rgba_bytes = image.astype(np.uint8).tobytes()
                
                # Create DDS header and combine with pixel data
                dds_header = create_dds_header(width, height, fourcc)
                dds_data = dds_header + rgba_bytes
                
                # Save the DDS file
                final_path = os.path.join("temp", "enhanced.dds")
                with open(final_path, "wb") as f:
                    f.write(dds_data)
            except Exception as e:
                st.error(f"Failed to convert to DDS: {str(e)}. Saving as PNG instead.")
                final_path = enhanced_png_path
        else:
            # For PNG or other formats, return the PNG path (extend for other formats if needed)
            final_path = enhanced_png_path

        return final_path

    except Exception as e:
        st.error(f"Error in enhance_texture: {str(e)}")
        return None



# File uploader
uploaded_file = st.file_uploader("Upload a .dds file", type=["dds"])
prompt = st.text_input(label="Enter your prompt", value="enhanced texture, preserve original pattern, realistic surface detail, ultra-sharp, high fidelity, photorealistic texture, seamless PBR quality, subtle lighting enhancement, microdetail preserved, high-resolution surface refinement, accurate color tones, enhanced normal map detail, surface imperfections, AAA game texture quality")

negative_prompt = st.text_input(label="Enter your Negaitive prompt", value="lowres, pixelated, voxel, 8-bit, blurry, noisy, glitch, artifact, distorted, deformed, extra limbs, low detail, messy, inconsistent, bad anatomy, wrong proportions, bad hands, overexposed, underexposed, jpeg artifacts, unrealistic shading")

if uploaded_file:
    filename = uploaded_file.name
    st.success(f"Uploaded: {filename}")
    
    # Use temporary directory for file operations
    with tempfile.TemporaryDirectory() as tmpdir:
        # Save uploaded DDS file
        dds_path = os.path.join(tmpdir, filename)
        with open(dds_path, "wb") as f:
            f.write(uploaded_file.read())
        
        # Convert DDS to PNG and extract metadata
        converter = AssetConverter()  # Assumes this handles DDS-to-PNG conversion
        png_path, metadata_path = converter.convert_to_png(dds_path)
        
        if png_path is None:
            st.error("Failed to convert DDS to PNG.")
        else:
            # Save metadata as JSON (assuming AssetConverter doesn't do this)
            try:
                metadata = {}
                with open(dds_path, "rb") as f:
                    header = f.read(128)  # Standard DDS header size
                    if header[:4] != b'DDS ':
                        raise ValueError("Invalid DDS file")
                    fourcc = header[84:88].decode("ascii", errors="ignore")
                    metadata["fourcc"] = fourcc
                
                meta_filename = os.path.splitext(filename)[0] + ".json"
                meta_path = os.path.join(tmpdir, meta_filename)
                with open(meta_path, "w") as f:
                    json.dump(metadata, f)
                st.success("Metadata extracted and saved.")
            except Exception as e:
                st.error(f"Failed to extract metadata: {e}")
                meta_path = None
            
            # Display original PNG
            st.image(png_path, caption="Original Texture", use_column_width=True)
            
            # Output format selection
            output_format = st.selectbox(
                "Select Output Format",
                ["PNG", "DDS"],
                help="Choose the format for the enhanced texture."
            ).lower()
            
            # Enhance button
            if st.button("Enhance Texture"):
                with st.spinner("Enhancing texture..."):
                    
                    enhanced_path = enhance_texture(
                        png_path,
                        prompt,
                        negative_prompt
                        output_format=output_format,
                        metadata_path=meta_path if output_format == 'dds' else None
                    )
                    
                    if enhanced_path:
                        st.success("Enhancement complete!")
                        if output_format == 'png':
                            st.image(enhanced_path, caption="Enhanced Texture", use_column_width=True)
                        else:
                            st.info("Enhanced texture saved as DDS.")
                        
                        # Provide download button
                        with open(enhanced_path, "rb") as f:
                            st.download_button(
                                label=f"Download Enhanced Texture as {output_format.upper()}",
                                data=f,
                                file_name=f"enhanced_{os.path.splitext(filename)[0]}.{output_format}",
                                mime="image/png" if output_format == 'png' else "application/octet-stream"
                            )
                    else:
                        st.error("Enhancement failed.")