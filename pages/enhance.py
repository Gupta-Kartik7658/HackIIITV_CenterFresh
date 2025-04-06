import streamlit as st
import re
import subprocess
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
def enhance_texture(file_path, prompt, denoising_strength=0.25, cfg_scale=4, steps=40, output_format=None, metadata_path=None):
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

st.title("Texture Enhancement Studio")

# Upload DDS or PNG
uploaded_file = st.file_uploader("Upload a .dds or .png file", type=["dds", "png","vtf"])

# Prompt input
prompt = st.text_input(
    label="Enter your prompt",
    value="enhanced texture, preserve original pattern, realistic surface detail, ultra-sharp, high fidelity, photorealistic texture, seamless PBR quality, subtle lighting enhancement, microdetail preserved, high-resolution surface refinement, accurate color tones, enhanced normal map detail, surface imperfections, AAA game texture quality"
)

st.subheader("🔧 Enhancement Settings")

cfg_scale = st.slider(
    "CFG Scale (Prompt Adherence)", 
    min_value=1, 
    max_value=20, 
    value=4, 
    help="Higher values stick more closely to the prompt"
)

denoising_strength = st.slider(
    "Denoising Strength", 
    min_value=0.0, 
    max_value=1.0, 
    value=0.25, 
    step=0.05,
    help="Controls how much of the original image is retained (0 = retain more original)"
)

steps = st.slider(
    "Sampling Steps", 
    min_value=10, 
    max_value=100, 
    value=40, 
    step=1,
    help="Higher steps can improve image quality but take longer"
)

patterns = {
    "version": r"Version:\s*v(\d+\.\d+)",
    "width": r"Width:\s*(\d+)",
    "height": r"Height:\s*(\d+)",
    "depth": r"Depth:\s*(\d+)",
    "frames": r"Frames:\s*(\d+)",
    "start_frame": r"Start Frame:\s*(\d+)",
    "faces": r"Faces:\s*(\d+)",
    "mipmaps": r"Mipmaps:\s*(\d+)",
    "flags": r"Flags:\s*(0x[0-9A-Fa-f]+)",
    "format": r"Format:\s*([^\n\r]+)",
    "reflectivity": r"Reflectivity:\s*([\d\.]+),\s*([\d\.]+),\s*([\d\.]+)"
}

if uploaded_file:
    filename = uploaded_file.name
    file_ext = filename.split(".")[-1].lower()
    st.success(f"Uploaded: {filename}")

    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, filename)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        if file_ext == "dds":
            # Convert DDS to PNG and extract metadata
            converter = AssetConverter()
            png_path, _ = converter.convert_to_png(file_path)

            if png_path is None:
                st.error("❌ Failed to convert DDS to PNG.")
            else:
                try:
                    metadata = {}
                    with open(file_path, "rb") as f:
                        header = f.read(128)
                        if header[:4] != b'DDS ':
                            raise ValueError("Invalid DDS file")
                        fourcc = header[84:88].decode("ascii", errors="ignore")
                        metadata["fourcc"] = fourcc

                    meta_filename = os.path.splitext(filename)[0] + ".json"
                    meta_path = os.path.join(tmpdir, meta_filename)
                    with open(meta_path, "w") as f:
                        json.dump(metadata, f)

                    st.success("✅ Metadata extracted and saved.")
                except Exception as e:
                    st.error(f"❌ Failed to extract metadata: {e}")
                    meta_path = None
                
        elif file_ext == "vtf":
            vtf_file = file_path
            vtfcmd_path = r"vtflib132-bin/bin/x64/VTFCmd.exe"
            
            result = subprocess.run(
                [vtfcmd_path, "-file", vtf_file , "-output", tmpdir ,"-exportformat","png"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            output = result.stdout
            metadata = {}
            for key, pattern in patterns.items():
                match = re.search(pattern, output)
                if match:
                    if key == "reflectivity":
                        metadata[key] = {
                            "r": float(match.group(1)),
                            "g": float(match.group(2)),
                            "b": float(match.group(3))
                        }
                    elif key in ["width", "height", "depth", "frames", "start_frame", "faces", "mipmaps"]:
                        metadata[key] = int(match.group(1))
                    elif key == "version":
                        metadata[key] = float(match.group(1))
                    else:
                        metadata[key] = match.group(1).strip()

            # Save metadata JSON
            meta_filename = os.path.splitext(filename)[0] + ".json"
            meta_path = os.path.join(tmpdir, meta_filename)
            with open(meta_path, "w") as f:
                json.dump(metadata, f, indent=4)

            # ✅ Set the converted PNG path
            converted_png_name = os.path.splitext(filename)[0] + ".png"
            png_path = os.path.join(tmpdir, converted_png_name)

            
        elif file_ext == "png":
            png_path = file_path
            meta_path = None  # No metadata available for PNGs

        # Show original texture
        image = Image.open(png_path)
        st.image(image, caption="🧩 Original Texture", use_column_width=True)

        # Output format selection
        output_format = st.selectbox(
            "Select Output Format",
            ["PNG", "DDS"],
            help="Choose the format for the enhanced texture."
        ).lower()

        if st.button("Enhance Texture"):
            with st.spinner("✨ Enhancing texture..."):

                enhanced_path = enhance_texture(
                    png_path,
                    prompt,
                    denoising_strength=denoising_strength,
                    cfg_scale=cfg_scale,
                    steps=steps,
                    output_format=output_format,
                    metadata_path=meta_path if output_format == 'dds' else None
                )

                if enhanced_path:
                    st.success("🎉 Enhancement complete!")

                    if output_format == 'png':
                        st.image(Image.open(enhanced_path), caption="✨ Enhanced Texture", use_column_width=True)
                    else:
                        st.info("Enhanced texture saved as DDS.")

                    with open(enhanced_path, "rb") as f:
                        st.download_button(
                            label=f"⬇️ Download Enhanced Texture as {output_format.upper()}",
                            data=f,
                            file_name=f"enhanced_{os.path.splitext(filename)[0]}.{output_format}",
                            mime="image/png" if output_format == 'png' else "application/octet-stream"
                        )
                else:
                    st.error("❌ Enhancement failed.")