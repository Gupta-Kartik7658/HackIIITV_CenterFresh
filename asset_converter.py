import os
import subprocess
import imageio
import json
from pathlib import Path
from PIL import Image
import numpy as np
import requests
import base64

class AssetConverter:
    def __init__(self, vtflib_path="vtflib132-bin/bin/x64/VTFCmd.exe"):
        """
        Initialize the asset converter with paths to necessary tools.
        
        Args:
            vtflib_path: Path to VTFCmd.exe for VTF conversion
        """
        self.vtflib_path = vtflib_path
        
        # Create necessary directories
        self.temp_dir = Path("temp")
        self.temp_dir.mkdir(exist_ok=True)
        os.makedirs("output", exist_ok=True)
        
    def dds_to_png(self, dds_path):
        """
        Convert a DDS file to PNG.
        
        Args:
            dds_path: Path to the DDS file
            
        Returns:
            Path to the converted PNG file
        """
        try:
            # Load image using imageio
            image = imageio.imread(dds_path, format='dds')
            
            # Save as PNG
            png_filename = os.path.splitext(os.path.basename(dds_path))[0] + ".png"
            png_path = self.temp_dir / png_filename
            imageio.imwrite(png_path, image, format='png')
            
            # Extract and save metadata
            metadata = self._extract_dds_metadata(dds_path)
            meta_filename = os.path.splitext(os.path.basename(dds_path))[0] + ".json"
            meta_path = self.temp_dir / meta_filename
            with open(meta_path, "w") as f:
                json.dump(metadata, f, indent=2)
                
            return png_path, meta_path
        except Exception as e:
            print(f"Error converting DDS to PNG: {str(e)}")
            return None, None
    
    def vtf_to_png(self, vtf_path):
        """
        Convert a VTF file to PNG using VTFCmd.
        
        Args:
            vtf_path: Path to the VTF file
            
        Returns:
            Path to the converted PNG file
        """
        try:
            # Use VTFCmd to convert VTF to PNG
            png_filename = os.path.splitext(os.path.basename(vtf_path))[0] + ".png"
            png_path = self.temp_dir / png_filename
            
            subprocess.run([
                self.vtflib_path,
                "-file", vtf_path,
                "-output", str(png_path),
                "-exportformat", "png"
            ], check=True)
            
            # Extract and save metadata
            metadata = self._extract_vtf_metadata(vtf_path)
            meta_filename = os.path.splitext(os.path.basename(vtf_path))[0] + ".json"
            meta_path = self.temp_dir / meta_filename
            with open(meta_path, "w") as f:
                json.dump(metadata, f, indent=2)
                
            return png_path, meta_path
        except Exception as e:
            print(f"Error converting VTF to PNG: {str(e)}")
            return None, None
    
    def png_to_dds(self, png_path, metadata_path=None, output_path=None):
        """
        Convert a PNG file back to DDS using the original metadata.
        
        Args:
            png_path: Path to the PNG file
            metadata_path: Path to the metadata JSON file
            output_path: Path to save the DDS file (optional)
            
        Returns:
            Path to the converted DDS file
        """
        try:
            # Load metadata if provided
            metadata = {}
            if metadata_path and os.path.exists(metadata_path):
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
            
            # Load PNG image
            img = Image.open(png_path)
            img_array = np.array(img)
            
            # Determine output path
            if output_path is None:
                output_path = os.path.splitext(png_path)[0] + ".dds"
            
            # Get format from metadata or use default
            format_str = metadata.get('format', 'DXT5')
            
            # Convert format string to imageio format
            format_map = {
                'DXT1': 'dxt1',
                'DXT3': 'dxt3',
                'DXT5': 'dxt5',
                'BC7': 'bc7'
            }
            dds_format = format_map.get(format_str.upper(), 'dxt5')
            
            # Save as DDS
            imageio.imwrite(output_path, img_array, format='dds', compression=dds_format)
            
            return output_path
        except Exception as e:
            print(f"Error converting PNG to DDS: {str(e)}")
            return None
    
    def png_to_vtf(self, png_path, metadata_path=None, output_path=None):
        """
        Convert a PNG file back to VTF using VTFCmd.
        
        Args:
            png_path: Path to the PNG file
            metadata_path: Path to the metadata JSON file
            output_path: Path to save the VTF file (optional)
            
        Returns:
            Path to the converted VTF file
        """
        try:
            # Load metadata if provided
            metadata = {}
            if metadata_path and os.path.exists(metadata_path):
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
            
            # Determine output path
            if output_path is None:
                output_path = os.path.splitext(png_path)[0] + ".vtf"
            
            # Get format from metadata or use default
            format_str = metadata.get('format', 'DXT5')
            
            # Convert format string to VTFCmd format
            format_map = {
                'DXT1': 'dxt1',
                'DXT3': 'dxt3',
                'DXT5': 'dxt5',
                'BC7': 'bc7'
            }
            vtf_format = format_map.get(format_str.upper(), 'dxt5')
            
            # Build VTFCmd command
            cmd = [
                self.vtflib_path,
                "-file", png_path,
                "-output", output_path,
                "-format", vtf_format,
                "-resize", "1",  # No resize
                "-normal", "0",  # Not a normal map
                "-mipmaps", "1"  # Generate mipmaps
            ]
            
            # Add additional options from metadata if available
            if 'flags' in metadata:
                cmd.extend(["-flags", str(metadata['flags'])])
            if 'bumpmap' in metadata:
                cmd.extend(["-bumpmap", str(metadata['bumpmap'])])
            
            # Run VTFCmd
            subprocess.run(cmd, check=True)
            
            return output_path
        except Exception as e:
            print(f"Error converting PNG to VTF: {str(e)}")
            return None
    
    def _extract_dds_metadata(self, dds_path):
        """
        Extract metadata from a DDS file.
        
        Args:
            dds_path: Path to the DDS file
            
        Returns:
            Dictionary containing metadata
        """
        try:
            metadata = {}
            with open(dds_path, "rb") as f:
                header = f.read(128)  # Standard DDS header
                if header[0:4] != b'DDS ':
                    raise ValueError("Invalid DDS magic number")

                # Extract basic information
                metadata["magic"] = "DDS "
                metadata["header_hex"] = header.hex()
                
                # Extract dimensions
                metadata["width"] = int.from_bytes(header[12:16], 'little')
                metadata["height"] = int.from_bytes(header[16:20], 'little')
                
                # Extract format information
                fourcc = header[84:88]
                fourcc_str = fourcc.decode("ascii", errors="ignore")
                metadata["fourcc"] = fourcc_str
                
                # Map FourCC to format name
                format_map = {
                    'DXT1': 'DXT1',
                    'DXT3': 'DXT3',
                    'DXT5': 'DXT5',
                    'DX10': 'BC7'
                }
                metadata["format"] = format_map.get(fourcc_str, 'DXT5')

                # Check for DX10 extended header
                if fourcc_str == "DX10":
                    dx10_header = f.read(20)
                    metadata["dx10_header_hex"] = dx10_header.hex()
                    metadata["has_dx10_header"] = True
                    # Extract additional DX10 format information
                    dx10_format = int.from_bytes(dx10_header[0:4], 'little')
                    metadata["dx10_format"] = dx10_format
                else:
                    metadata["has_dx10_header"] = False

            return metadata
        except Exception as e:
            print(f"Error extracting DDS metadata: {str(e)}")
            return {"format": "DXT5"}  # Return default format if extraction fails
    
    def _extract_vtf_metadata(self, vtf_path):
        """
        Extract metadata from a VTF file using VTFCmd.
        
        Args:
            vtf_path: Path to the VTF file
            
        Returns:
            Dictionary containing metadata
        """
        try:
            metadata = {"format": "vtf", "source": vtf_path}
            
            # Create a temporary info file
            info_path = os.path.splitext(vtf_path)[0] + "_info.txt"
            
            # Run VTFCmd to get VTF information
            subprocess.run([
                self.vtflib_path,
                "-file", vtf_path,
                "-info",
                "-output", info_path
            ], check=True)
            
            # Read the info file
            if os.path.exists(info_path):
                with open(info_path, 'r') as f:
                    info_text = f.read()
                    
                    # Extract format
                    if "DXT1" in info_text:
                        metadata["format"] = "DXT1"
                    elif "DXT3" in info_text:
                        metadata["format"] = "DXT3"
                    elif "DXT5" in info_text:
                        metadata["format"] = "DXT5"
                    elif "BC7" in info_text:
                        metadata["format"] = "BC7"
                    
                    # Extract flags
                    if "NORMAL" in info_text:
                        metadata["flags"] = "NORMAL"
                    if "BUMPMAP" in info_text:
                        metadata["bumpmap"] = True
                    
                    # Extract dimensions
                    import re
                    width_match = re.search(r"Width:\s*(\d+)", info_text)
                    height_match = re.search(r"Height:\s*(\d+)", info_text)
                    if width_match:
                        metadata["width"] = int(width_match.group(1))
                    if height_match:
                        metadata["height"] = int(height_match.group(1))
                
                # Clean up info file
                os.remove(info_path)
            
            return metadata
        except Exception as e:
            print(f"Error extracting VTF metadata: {str(e)}")
            return {"format": "DXT5"}  # Return default format if extraction fails
    
    def convert_to_png(self, file_path):
        """
        Convert a game asset file to PNG based on its extension.
        
        Args:
            file_path: Path to the game asset file
            
        Returns:
            Path to the converted PNG file and metadata file
        """
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.dds':
            return self.dds_to_png(file_path)
        elif ext == '.vtf':
            return self.vtf_to_png(file_path)
        else:
            print(f"Unsupported file format: {ext}")
            return None, None
    
    def convert_from_png(self, png_path, original_format, metadata_path=None, output_path=None):
        """
        Convert a PNG file back to the original game asset format.
        
        Args:
            png_path: Path to the PNG file
            original_format: Original format ('dds' or 'vtf')
            metadata_path: Path to the metadata JSON file
            output_path: Path to save the output file (optional)
            
        Returns:
            Path to the converted file
        """
        if original_format.lower() == 'dds':
            return self.png_to_dds(png_path, metadata_path, output_path)
        elif original_format.lower() == 'vtf':
            return self.png_to_vtf(png_path, metadata_path, output_path)
        else:
            print(f"Unsupported format: {original_format}")
            return None

    def enhance_image(self, png_path, denoising_strength, cfg_scale, steps):
        """
        Enhance an image using Stable Diffusion.
        
        Args:
            png_path: Path to the PNG file
            denoising_strength: Denoising strength for Stable Diffusion
            cfg_scale: CFG scale for Stable Diffusion
            steps: Steps for Stable Diffusion
            
        Returns:
            Path to the enhanced PNG file
        """
        try:
            # Encode the image as base64
            with open(png_path, "rb") as f:
                encoded_image = base64.b64encode(f.read()).decode("utf-8")

            # Send request to Stable Diffusion API
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

            # Decode the response
            enhanced_image = base64.b64decode(response.json()["images"][0])

            # Save the enhanced image
            enhanced_filename = os.path.splitext(os.path.basename(png_path))[0] + "_enhanced.png"
            enhanced_path = self.temp_dir / enhanced_filename
            with open(enhanced_path, "wb") as f:
                f.write(enhanced_image)

            return enhanced_path
        except Exception as e:
            print(f"Error enhancing image: {str(e)}")
            return None

    def check_file_size(self, uploaded_file):
        """
        Check if the file size is under 25KB.
        
        Args:
            uploaded_file: The uploaded file object
            
        Returns:
            True if the file size is under 25KB, False otherwise
        """
        if uploaded_file.size > 25000:
            print(f"{uploaded_file.name} is too large! Please upload files under 25KB.")
            return False
        return True 