import streamlit as st

# Load global CSS
with open("C:\Documents\HackIIITV25\HackIIITV_CenterFresh\styles\global.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown('<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">', unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-title">Settings</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Customize Your Experience</p>', unsafe_allow_html=True)

# Settings form
st.markdown('<h2 class="section-title">Enhancement Options</h2>', unsafe_allow_html=True)
with st.form("settings_form"):
    sharpness = st.slider("Sharpness", 0.0, 2.0, 1.0, step=0.1)
    contrast = st.slider("Contrast", 0.5, 1.5, 1.0, step=0.1)
    style = st.selectbox("Style Preset", ["Default", "GTA V", "Cyberpunk", "Nintendo Modern"])
    submit = st.form_submit_button("Save Settings")
    if submit:
        st.success("Settings saved! (Note: Apply these in Enhance page for now.)")

# Sidebar
st.sidebar.title("Navigation")
st.sidebar.button("Back to About", on_click=lambda: st.switch_page("../app.py"))
st.sidebar.button("Enhance Textures", on_click=lambda: st.switch_page("enhance.py"))
st.sidebar.button("Gallery", on_click=lambda: st.switch_page("gallery.py"))
st.sidebar.button("Tutorial", on_click=lambda: st.switch_page("tutorial.py"))
st.sidebar.markdown('<p class="text">Tweak your remastering process!</p>', unsafe_allow_html=True)