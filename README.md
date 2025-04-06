Here’s an updated version of your `README.md` with the requested additions for:

- Stable Diffusion model (Realistic Vision v5.1)
- AUTOMATIC1111 WebUI repo
- ControlNet model files (Canny & Lineart)
- ControlNet extension

---

# Game Texture Enhancement Tool

A tool for enhancing legacy game textures using AI/ML models. This application helps game designers recreate and enhance texture packs for remastered games.

## Features

- Support for multiple texture formats (PNG, DDS, VTF)  
- AI-powered texture enhancement using Stable Diffusion  
- Metadata preservation for game assets  
- User-friendly interface with real-time preview  
- Customizable enhancement parameters  

## Prerequisites

1. Python 3.8 or higher  
2. Stable Diffusion WebUI running locally  
3. VTFCmd.exe for VTF file handling  
4. **Model files and extensions listed below**

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download VTFCmd:
- Download VTFCmd from the official Source SDK
- Place `VTFCmd.exe` in the `vtflib132-bin/bin/x64/` directory

4. Set up Stable Diffusion WebUI:
- Clone and install from [AUTOMATIC1111 WebUI repo](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
- Ensure the WebUI is running on http://127.0.0.1:7860

5. Download Stable Diffusion & ControlNet Models:

### 🧠 Stable Diffusion Model

- [Realistic Vision v5.1 (SD 1.5)](https://civitai.com/models/4201/realistic-vision-v51)
  - Place it in: `stable-diffusion-webui/models/Stable-diffusion/`

### 🔌 ControlNet Extension

- Install the ControlNet extension from the WebUI:
  - Go to Extensions → Available → Search "ControlNet"
  - Install and restart WebUI

### 📦 ControlNet Models

- [Canny Model](https://huggingface.co/lllyasviel/ControlNet-v1-1/blob/main/control_v11p_sd15_canny.pth)
- [Lineart Model](https://huggingface.co/lllyasviel/ControlNet-v1-1/blob/main/control_v11p_sd15_lineart.pth)  
  - Place them in: `stable-diffusion-webui/extensions/sd-webui-controlnet/models/`

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Upload a texture file (PNG, DDS, or VTF)  
3. Provide a prompt as per your choice of enhancements
4. Adjust enhancement parameters:
   - Denoising Strength (0.0 to 1.0)
   - CFG Scale (1 to 20)
   - Steps (1 to 150)
5. Select output format  
6. Click "Enhance Texture"  
7. Download the enhanced texture  

## File Size Limits 
- Supported formats: PNG, DDS, VTF  
- Output formats: PNG, DDS 

## Troubleshooting

1. **Stable Diffusion WebUI Connection Error**
   - Ensure the WebUI is running on http://127.0.0.1:7860
   - Check if the API is accessible

2. **VTF Conversion Issues**
   - Verify VTFCmd.exe is in the correct location
   - Check file permissions

3. **Large File Errors**
   - Reduce file size or use a smaller texture
   - Consider splitting large textures
