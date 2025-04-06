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
- Place VTFCmd.exe in the `vtflib132-bin/bin/x64/` directory

4. Set up Stable Diffusion WebUI:
- Follow the [Stable Diffusion WebUI installation guide](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
- Ensure the WebUI is running on http://127.0.0.1:7860

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Upload a texture file (PNG, DDS, or VTF)
3. Adjust enhancement parameters:
   - Denoising Strength (0.0 to 1.0)
   - CFG Scale (1 to 20)
   - Steps (1 to 150)
4. Select output format
5. Click "Enhance Texture"
6. Download the enhanced texture

## File Size Limits

- Maximum file size: 25KB
- Supported formats: PNG, DDS, VTF
- Output formats: PNG, DDS, VTF

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

## Contributing

Feel free to submit issues and enhancement requests!

## License

[Your License Here]
