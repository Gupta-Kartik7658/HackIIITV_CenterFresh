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

# Sidebar
with st.sidebar:
    st.image("assets/logo.png", use_column_width=True)
    st.markdown('<h2 style="text-align: center; color: #FFD700; text-shadow: 2px 2px #FF4B4B;">Texture Remaster Tool</h2>', unsafe_allow_html=True)
    
    st.markdown('<div style="background-color: rgba(42, 42, 42, 0.7); padding: 15px; border-radius: 10px; margin: 20px 0;">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #FF4B4B; text-align: center;">Navigation</h3>', unsafe_allow_html=True)
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("app.py")
    if st.button("🎨 Enhance Textures", use_container_width=True):
        st.switch_page("pages/enhance.py")
    if st.button("🖼️ Gallery", use_container_width=True):
        st.switch_page("pages/gallery.py")
    if st.button("⚙️ Settings", use_container_width=True):
        st.switch_page("pages/settings.py")
    if st.button("📖 Tutorial", use_container_width=True):
        st.switch_page("pages/tutorial.py")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div style="background-color: rgba(42, 42, 42, 0.7); padding: 15px; border-radius: 10px; margin: 20px 0;">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #FF4B4B; text-align: center;">About</h3>', unsafe_allow_html=True)
    st.markdown('<p style="color: #E0E0E0; text-align: center;">Transform retro game textures into modern masterpieces using AI technology.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div style="margin-top: auto; text-align: center; padding: 20px;">', unsafe_allow_html=True)
    st.markdown('<p style="color: #E0E0E0;">Crafted with ❤️ by CenterFresh</p>', unsafe_allow_html=True)
    st.markdown('<p style="color: #E0E0E0;">Hackathon 2025</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Main content
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

# Footer
st.markdown("""
    <hr style="border: 2px dashed #FFD700; margin: 40px 0;">
    <p class="text" style="text-align: center;">Crafted with ❤️ by Team: CenterFresh | Hackathon 2025</p>
    <p class="text" style="text-align: center;">Team Members: </p>
    <p class="text" style="text-align: center;"> Kartik </p>
    <p class="text" style="text-align: center;"> Abhinav</p>
    <p class="text" style="text-align: center;"> Abhijeet</p>
    <p class="text" style="text-align: center;"> Ankit</p>
""", unsafe_allow_html=True)