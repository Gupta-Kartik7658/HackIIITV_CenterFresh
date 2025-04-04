import streamlit as st
from PIL import Image
import os
from pathlib import Path
from enhance import enhance_texture  # Placeholder for AI logic

# Set up directories
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Streamlit app
st.title("Texture Remaster Tool")
st.markdown("Upload a legacy game texture and enhance it with AI!")

# File uploader (simulates drag-and-drop)
uploaded_file = st.file_uploader("Drop or select a texture file", type=["png", "jpg", "jpeg"], key="texture_uploader")

# Process and display
if uploaded_file is not None:
    # Save the uploaded file
    file_path = UPLOAD_DIR / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Display original texture
    st.subheader("Original Texture")
    original_img = Image.open(file_path)
    st.image(original_img, use_column_width=True)

    # Enhance button
    if st.button("Enhance Texture"):
        with st.spinner("Enhancing texture with AI..."):
            # Call the enhancement function (placeholder)
            enhanced_path = enhance_texture(file_path)
            enhanced_img = Image.open(enhanced_path)
            
            # Display enhanced texture
            st.subheader("Enhanced Texture")
            st.image(enhanced_img, use_column_width=True)
            
            # Download option
            with open(enhanced_path, "rb") as f:
                st.download_button(
                    label="Download Enhanced Texture",
                    data=f,
                    file_name=f"enhanced_{uploaded_file.name}",
                    mime="image/png"
                )

# Sidebar with info
st.sidebar.title("About")
st.sidebar.info("A tool for designers to remaster old game textures using AI. Upload a texture, enhance it, and download the result!")