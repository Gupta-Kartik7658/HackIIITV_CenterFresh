import streamlit as st
from PIL import Image
from pathlib import Path
from enhance_backend import enhance_texture
import os
import tempfile
import json
import imageio

# Load global CSS
css_path = Path("styles/global.css")
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
else:
    st.error("CSS file not found. Please check the styles directory.")

st.markdown('<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">', unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-title">Enhance Your Textures</h1>', unsafe_allow_html=True)

# Drag-and-drop area with batch support
st.markdown('<div class="dropzone"><p class="dropzone-text">Drag & Drop or Click to Upload<br>(PNG, DDS, VTF, ~20KB, Multiple Files Supported)</p></div>', unsafe_allow_html=True)

def extract_dds_metadata(dds_path):
    metadata = {}
    with open(dds_path, "rb") as f:
        header = f.read(128)  # Standard DDS header
        if header[0:4] != b'DDS ':
            raise ValueError("Invalid DDS magic number")

        fourcc = header[84:88]
        fourcc_str = fourcc.decode("ascii", errors="ignore")
        metadata["magic"] = "DDS "
        metadata["header_hex"] = header.hex()
        metadata["fourcc"] = fourcc_str

        if fourcc_str == "DX10":
            dx10_header = f.read(20)
            metadata["dx10_header_hex"] = dx10_header.hex()
            metadata["has_dx10_header"] = True
        else:
            metadata["has_dx10_header"] = False

    return metadata

# st.title("DDS → PNG + Metadata Extractor")
uploaded_file = st.file_uploader("Upload a .dds file", type=["dds"])

if uploaded_file:
    filename = uploaded_file.name
    st.success(f"Uploaded: {filename}")

    # Save uploaded file temporarily
    with tempfile.TemporaryDirectory() as tmpdir:
        dds_path = os.path.join(tmpdir, filename)
        with open(dds_path, "wb") as f:
            f.write(uploaded_file.read())

        # Convert DDS to PNG
        try:
            image = imageio.imread(dds_path, format='dds')
            png_filename = os.path.splitext(filename)[0] + ".png"
            png_path = os.path.join(tmpdir, png_filename)
            imageio.imwrite(png_path, image, format='png')

            st.image(png_path, caption="Converted PNG", use_column_width=True)
            st.download_button("Download PNG", open(png_path, "rb"), file_name=png_filename)
        except Exception as e:
            st.error(f"❌ Failed to convert DDS to PNG: {e}")

        # Extract Metadata
        try:
            metadata = extract_dds_metadata(dds_path)
            st.json(metadata)
            meta_filename = os.path.splitext(filename)[0] + ".json"
            meta_path = os.path.join(tmpdir, meta_filename)
            with open(meta_path, "w") as f:
                json.dump(metadata, f, indent=2)
            st.download_button("Download Metadata JSON", open(meta_path, "rb"), file_name=meta_filename)
        except Exception as e:
            st.error(f"❌ Failed to extract metadata: {e}")
            
# Set up directories
UPLOAD_DIR = Path("../uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Stable Diffusion settings
st.markdown('<h2 class="section-title">Stable Diffusion Settings</h2>', unsafe_allow_html=True)
denoising_strength = st.slider("Denoising Strength", min_value=0.0, max_value=1.0, value=0.75, step=0.05, 
                              help="Controls how much the image is changed. Higher values create more variation.")
cfg_scale = st.slider("CFG Scale", min_value=1, max_value=20, value=7, step=1,
                      help="Controls how closely the image follows the prompt. Higher values make it more literal.")
steps = st.number_input("Steps", min_value=1, max_value=150, value=30, step=1,
                       help="Number of diffusion steps. More steps can improve quality but take longer.")

# Output format settings
st.markdown('<h2 class="section-title">Output Format</h2>', unsafe_allow_html=True)
output_format = st.selectbox(
    "Select Output Format",
    ["PNG", "DDS", "VTF"],
    help="Choose the format for the enhanced texture. If you uploaded a game asset, select the same format to maintain compatibility."
)

# Process and display
if uploaded_file:
    st.markdown('<h2 class="section-title">Preview</h2>', unsafe_allow_html=True)
    file_path = UPLOAD_DIR / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Determine original format
    original_format = os.path.splitext(uploaded_file.name)[1].lower()[1:] if os.path.splitext(uploaded_file.name)[1].lower() in ['.dds', '.vtf'] else 'png'
    
    tab1, tab2 = st.tabs([f"{uploaded_file.name} - Original", f"{uploaded_file.name} - Enhanced"])
    with tab1:
        st.markdown('<div class="image-box">', unsafe_allow_html=True)
        st.write("Original Texture")
        
        # Display original image
        if original_format in ['dds', 'vtf']:
            st.info(f"This is a {original_format.upper()} file. It will be converted to PNG for enhancement.")
            # We can't directly display DDS/VTF files, so show a placeholder
            st.image("assets/placeholder.png", use_column_width=True)
        else:
            original_img = Image.open(file_path)
            st.image(original_img, use_column_width=True)
            
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button(f"Enhance {uploaded_file.name}", key=f"enhance_{uploaded_file.name}"):
        with st.spinner(f"Remastering {uploaded_file.name}..."):
            # Convert output format to lowercase for the backend
            output_format_lower = output_format.lower()
            
            # If the original format is a game asset and the output format is PNG,
            # we need to specify the original format for proper conversion
            if original_format in ['dds', 'vtf'] and output_format_lower == 'png':
                enhanced_path = enhance_texture(file_path, denoising_strength, cfg_scale, steps)
            else:
                enhanced_path = enhance_texture(file_path, denoising_strength, cfg_scale, steps, output_format_lower)
            
            if enhanced_path:
                # Display enhanced image
                with tab2:
                    st.markdown('<div class="image-box">', unsafe_allow_html=True)
                    st.write("Enhanced Texture")
                    
                    if output_format_lower in ['dds', 'vtf']:
                        st.info(f"Enhanced texture saved as {output_format.upper()}. You can download it below.")
                        # Show a placeholder for DDS/VTF files
                        st.image("assets/placeholder.png", use_column_width=True)
                    else:
                        enhanced_img = Image.open(enhanced_path)
                        st.image(enhanced_img, use_column_width=True)
                        
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Download button
                with open(enhanced_path, "rb") as f:
                    st.download_button(
                        label=f"Download Enhanced {uploaded_file.name.split('.')[0]} as {output_format}",
                        data=f,
                        file_name=f"enhanced_{uploaded_file.name.split('.')[0]}.{output_format_lower}",
                        mime=f"image/{output_format_lower}"
                    )
            else:
                st.error("Enhancement failed. Please check if Stable Diffusion WebUI is running.")