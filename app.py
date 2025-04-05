import streamlit as st
from pathlib import Path

# Set page config (first command)
st.set_page_config(
    page_title="Texture Remaster Tool",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load global CSS
css_path = Path("styles/global.css")
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
else:
    st.error("CSS file not found. Please check the styles directory.")

# Add Google font
st.markdown('<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">', unsafe_allow_html=True)

# Logo and Header
col1, col2 = st.columns([1, 3])
with col1:
    st.image("assets/logo.png", use_column_width=True)
with col2:
    st.markdown('<h1 class="main-title">Texture Remaster Tool</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Reviving Retro Games with AI Magic</p>', unsafe_allow_html=True)

# About section
st.markdown('<h2 class="section-title">Our Mission</h2>', unsafe_allow_html=True)
with st.container():
    st.markdown("""
        <div class="image-box" style="padding: 20px;">
            <p class="text">
            Welcome to the Texture Remaster Tool—a fusion of nostalgia and innovation. We're here to transform the pixelated sprites of classics like <i>GTA Vice City</i> and Nintendo gems into stunning, modern game assets. Powered by Stable Diffusion AI, our tool reimagines retro textures for today's game engines with unprecedented quality and detail.
            </p>
        </div>
    """, unsafe_allow_html=True)

# Examples section
st.markdown('<h2 class="section-title">Before & After</h2>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.image("assets/before_after1.png", caption="Pixel to Polished", use_column_width=True)
with col2:
    st.image("assets/before_after2.png", caption="Retro to Refined", use_column_width=True)

# Navigation
st.markdown('<h2 class="section-title">Explore More</h2>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("Enhance Textures"):
        st.switch_page("pages/enhance.py")
with col2:
    if st.button("Gallery"):
        st.switch_page("pages/gallery.py")
with col3:
    if st.button("Settings"):
        st.switch_page("pages/settings.py")
with col4:
    if st.button("Tutorial"):
        st.switch_page("pages/tutorial.py")

# Footer
st.markdown("""
    <hr style="border: 2px dashed #FFD700; margin: 40px 0;">
    <p class="text" style="text-align: center;">Crafted with ❤️ by CenterFresh | Hackathon 2025</p>
""", unsafe_allow_html=True)