import streamlit as st

# Load global CSS
with open("C:\Documents\HackIIITV25\HackIIITV_CenterFresh\styles\global.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown('<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">', unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-title">Gallery</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Explore AI-Remastered Masterpieces</p>', unsafe_allow_html=True)

# Gallery grid
st.markdown('<h2 class="section-title">Our Favorites</h2>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="image-box">', unsafe_allow_html=True)
    st.image("assets/before_after2.png", caption="Mario Image - Enhanced with Stable Diffusion", use_column_width=True)
    st.download_button("Download Sample", file_name="mario_enhanced.png", data=open("assets/before_after2.png", "rb"), mime="image/png")
    st.markdown('</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="image-box">', unsafe_allow_html=True)
    st.image("assets/before_after1.png", caption="Laser Fight - Enhanced with Stable Diffusion", use_column_width=True)
    st.download_button("Download Sample", file_name="vicecity_enhanced.png", data=open("assets/before_after1.png", "rb"), mime="image/png")
    st.markdown('</div>', unsafe_allow_html=True)