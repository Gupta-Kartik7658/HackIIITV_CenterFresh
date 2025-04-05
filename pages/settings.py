import streamlit as st

# Load global CSS
with open("C:\Documents\HackIIITV25\HackIIITV_CenterFresh\styles\global.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown('<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">', unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-title">Settings</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Customize Your Experience</p>', unsafe_allow_html=True)

# Settings form
st.markdown('<h2 class="section-title">Stable Diffusion Settings</h2>', unsafe_allow_html=True)
with st.form("settings_form"):
    denoising_strength = st.slider("Denoising Strength", 0.0, 1.0, 0.75, step=0.05, 
                                  help="Controls how much the image is changed. Higher values create more variation.")
    cfg_scale = st.slider("CFG Scale", 1, 20, 7, step=1,
                          help="Controls how closely the image follows the prompt. Higher values make it more literal.")
    steps = st.number_input("Steps", 1, 150, 30, step=1,
                           help="Number of diffusion steps. More steps can improve quality but take longer.")
    prompt = st.text_area("Default Prompt", "semi-realistic pixel art remaster, detailed, high-res",
                         help="The prompt used to guide the image generation.")
    submit = st.form_submit_button("Save Settings")
    if submit:
        st.success("Settings saved! These will be used as defaults in the Enhance page.")