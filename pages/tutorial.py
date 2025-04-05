import streamlit as st

# Load global CSS
with open("C:\Documents\HackIIITV25\HackIIITV_CenterFresh\styles\global.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown('<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">', unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-title">Tutorial</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Learn to Remaster Like a Pro</p>', unsafe_allow_html=True)

# Steps
st.markdown('<h2 class="section-title">How to Use</h2>', unsafe_allow_html=True)
with st.expander("Step 1: Find Retro Textures"):
    st.markdown('<p class="text">Grab low-res sprites from <a href="https://www.models-resource.com" target="_blank">The Models Resource</a> or your favorite retro game.</p>', unsafe_allow_html=True)
with st.expander("Step 2: Upload & Enhance"):
    st.markdown('<p class="text">Head to the Enhance page, drag your PNGs (~20KB), and click "Enhance Now"!</p>', unsafe_allow_html=True)
with st.expander("Step 3: Configure Settings"):
    st.markdown('''
    <p class="text">
    Adjust the Stable Diffusion settings to get the best results:
    <ul>
        <li><strong>Denoising Strength:</strong> Controls how much the image is changed (0.0-1.0)</li>
        <li><strong>CFG Scale:</strong> Controls how closely the image follows the prompt (1-20)</li>
        <li><strong>Steps:</strong> Number of diffusion steps (1-150)</li>
    </ul>
    </p>
    ''', unsafe_allow_html=True)
with st.expander("Step 4: Download & Use"):
    st.markdown('<p class="text">Choose PNG or TGA, download, and import into your game engine.</p>', unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Navigation")
st.sidebar.button("Back to About", on_click=lambda: st.switch_page("../app.py"))
st.sidebar.button("Enhance Textures", on_click=lambda: st.switch_page("enhance.py"))
st.sidebar.button("Gallery", on_click=lambda: st.switch_page("gallery.py"))
st.sidebar.button("Settings", on_click=lambda: st.switch_page("settings.py"))
st.sidebar.markdown('<p class="text">Get started with ease!</p>', unsafe_allow_html=True)