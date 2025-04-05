import streamlit as st
from pathlib import Path

# Load global CSS
css_path = Path("styles/global.css")
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
else:
    st.error("CSS file not found. Please check the styles directory.")

st.markdown('<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">', unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-title">How to Use</h1>', unsafe_allow_html=True)

# Step 1: Prepare Your Textures
st.markdown("""
<div class="tutorial-section">
    <h2 class="tutorial-title">Step 1: Prepare Your Textures</h2>
    <div class="tutorial-content">
        <p>Before you begin, make sure you have:</p>
        <ul>
            <li>Your texture files ready (PNG, DDS, or VTF format)</li>
            <li>Files should be under 25KB in size</li>
            <li>Stable Diffusion WebUI running locally</li>
        </ul>
        <p><strong>Note:</strong> For best results, use textures from retro games that you want to enhance.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Step 2: Upload Your Files
st.markdown("""
<div class="tutorial-section">
    <h2 class="tutorial-title">Step 2: Upload Your Files</h2>
    <div class="tutorial-content">
        <p>To upload your textures:</p>
        <ol>
            <li>Go to the "Enhance" page</li>
            <li>Click the upload area or drag and drop your files</li>
            <li>You can upload multiple files at once</li>
            <li>Supported formats: PNG, DDS, VTF</li>
        </ol>
        <p><strong>Tip:</strong> If your files are too large, consider splitting them into smaller textures.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Step 3: Configure Enhancement Settings
st.markdown("""
<div class="tutorial-section">
    <h2 class="tutorial-title">Step 3: Configure Enhancement Settings</h2>
    <div class="tutorial-content">
        <p>Adjust the Stable Diffusion parameters to control the enhancement:</p>
        <ul>
            <li><strong>Denoising Strength (0.0 - 1.0):</strong>
                <ul>
                    <li>Lower values (0.3-0.5): Subtle enhancements, preserves more of the original</li>
                    <li>Medium values (0.6-0.7): Balanced enhancement</li>
                    <li>Higher values (0.8-1.0): More dramatic changes, but may deviate from original style</li>
                </ul>
            </li>
            <li><strong>CFG Scale (1 - 20):</strong>
                <ul>
                    <li>Lower values (1-5): More creative, less constrained</li>
                    <li>Medium values (6-8): Good balance for most textures</li>
                    <li>Higher values (9-20): More literal interpretation of the prompt</li>
                </ul>
            </li>
            <li><strong>Steps (1 - 150):</strong>
                <ul>
                    <li>Lower values (1-20): Faster processing, less detailed</li>
                    <li>Medium values (30-50): Good balance of quality and speed</li>
                    <li>Higher values (60-150): Highest quality, but slower processing</li>
                </ul>
            </li>
        </ul>
        <p><strong>Recommended Settings for Beginners:</strong></p>
        <ul>
            <li>Denoising Strength: 0.75</li>
            <li>CFG Scale: 7</li>
            <li>Steps: 30</li>
        </ul>
    </div>
</div>
""", unsafe_allow_html=True)

# Step 4: Select Output Format
st.markdown("""
<div class="tutorial-section">
    <h2 class="tutorial-title">Step 4: Select Output Format</h2>
    <div class="tutorial-content">
        <p>Choose how you want your enhanced textures saved:</p>
        <ul>
            <li><strong>PNG:</strong> Universal format, good for preview and editing</li>
            <li><strong>DDS:</strong> DirectX texture format, used in many games</li>
            <li><strong>VTF:</strong> Valve Texture Format, used in Source engine games</li>
        </ul>
        <p><strong>Tip:</strong> If you're enhancing game assets, select the same format as the original for compatibility.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Step 5: Process and Download
st.markdown("""
<div class="tutorial-section">
    <h2 class="tutorial-title">Step 5: Process and Download</h2>
    <div class="tutorial-content">
        <p>After configuring your settings:</p>
        <ol>
            <li>Click the "Enhance" button for each texture</li>
            <li>Wait for the processing to complete (this may take a few minutes)</li>
            <li>Preview the enhanced texture in the interface</li>
            <li>Click the download button to save your enhanced texture</li>
        </ol>
        <p><strong>Note:</strong> Processing time depends on your settings and texture size.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Troubleshooting
st.markdown("""
<div class="tutorial-section">
    <h2 class="tutorial-title">Troubleshooting</h2>
    <div class="tutorial-content">
        <p>If you encounter issues:</p>
        <ul>
            <li><strong>Stable Diffusion WebUI not responding:</strong>
                <ul>
                    <li>Ensure it's running on http://127.0.0.1:7860</li>
                    <li>Check if the API is accessible</li>
                </ul>
            </li>
            <li><strong>File conversion errors:</strong>
                <ul>
                    <li>For VTF files: Ensure VTFCmd.exe is in the correct location</li>
                    <li>Check file permissions</li>
                </ul>
            </li>
            <li><strong>Large file errors:</strong>
                <ul>
                    <li>Reduce file size or use a smaller texture</li>
                    <li>Consider splitting large textures</li>
                </ul>
            </li>
        </ul>
    </div>
</div>
""", unsafe_allow_html=True)