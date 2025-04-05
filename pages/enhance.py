import streamlit as st
from PIL import Image
from pathlib import Path
from enhance_backend import enhance_texture

# Load global CSS
with open("C:\Documents\HackIIITV25\HackIIITV_CenterFresh\styles\global.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown('<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">', unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-title">Enhance Your Textures</h1>', unsafe_allow_html=True)

# Drag-and-drop area with batch support
st.markdown('<div class="dropzone"><p class="dropzone-text">Drag & Drop or Click to Upload<br>(PNG, ~20KB, Multiple Files Supported)</p></div>', unsafe_allow_html=True)
uploaded_files = st.file_uploader("", type=["png"], key="texture_uploader", label_visibility="collapsed", accept_multiple_files=True)
if uploaded_files:
    for uploaded_file in uploaded_files:
        if uploaded_file.size > 25000:
            st.error(f"{uploaded_file.name} is too large! Please upload PNGs under 25KB.")
            st.stop()

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

# Process and display
if uploaded_files:
    st.markdown('<h2 class="section-title">Preview</h2>', unsafe_allow_html=True)
    for uploaded_file in uploaded_files:
        file_path = UPLOAD_DIR / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        tab1, tab2 = st.tabs([f"{uploaded_file.name} - Original", f"{uploaded_file.name} - Enhanced"])
        with tab1:
            st.markdown('<div class="image-box">', unsafe_allow_html=True)
            st.write("Original Texture")
            original_img = Image.open(file_path)
            st.image(original_img, use_column_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        if st.button(f"Enhance {uploaded_file.name}", key=f"enhance_{uploaded_file.name}"):
            with st.spinner(f"Remastering {uploaded_file.name}..."):
                enhanced_path = enhance_texture(file_path, denoising_strength, cfg_scale, steps)
                if enhanced_path:
                    enhanced_img = Image.open(enhanced_path)
                    
                    with tab2:
                        st.markdown('<div class="image-box">', unsafe_allow_html=True)
                        st.write("Enhanced Texture")
                        st.image(enhanced_img, use_column_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    format_choice = st.selectbox("Choose Format", ["PNG", "TGA"], key=f"format_{uploaded_file.name}")
                    with open(enhanced_path, "rb") as f:
                        st.download_button(
                            label=f"Download {uploaded_file.name} as {format_choice}",
                            data=f,
                            file_name=f"enhanced_{uploaded_file.name.split('.')[0]}.{format_choice.lower()}",
                            mime=f"image/{format_choice.lower()}"
                        )
                else:
                    st.error("Enhancement failed. Please check if Stable Diffusion WebUI is running.")

# Sidebar
st.sidebar.title("Navigation")
st.sidebar.button("Back to About", on_click=lambda: st.switch_page("../app.py"))
st.sidebar.button("Gallery", on_click=lambda: st.switch_page("gallery.py"))
st.sidebar.button("Settings", on_click=lambda: st.switch_page("settings.py"))
st.sidebar.button("Tutorial", on_click=lambda: st.switch_page("tutorial.py"))
st.sidebar.markdown('<p class="text">Batch process your retro textures!</p>', unsafe_allow_html=True)