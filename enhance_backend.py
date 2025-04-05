import os.path as osp
import cv2
import numpy as np
import torch
import RRDBNet_arch as arch
from pathlib import Path

def enhance_texture(file_path):
    # Model setup
    model_path = 'models/RRDB_ESRGAN_x4.pth'
    device = torch.device('cpu')  # Change to 'cuda' if GPU is available
    model = arch.RRDBNet(3, 3, 64, 23, gc=32)
    model.load_state_dict(torch.load(model_path), strict=True)
    model.eval()
    model = model.to(device)

    # Prepare input
    input_dir = Path("LR")
    output_dir = Path("results")
    input_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)

    # Save uploaded file to LR folder
    base_name = osp.splitext(osp.basename(file_path))[0]
    lr_path = input_dir / f"{base_name}.png"
    img = cv2.imread(str(file_path), cv2.IMREAD_COLOR)
    cv2.imwrite(str(lr_path), img)

    # Process image
    img = img * 1.0 / 255
    img = torch.from_numpy(np.transpose(img[:, :, [2, 1, 0]], (2, 0, 1))).float()
    img_LR = img.unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(img_LR).data.squeeze().float().cpu().clamp_(0, 1).numpy()
    output = np.transpose(output[[2, 1, 0], :, :], (1, 2, 0))
    output = (output * 255.0).round()

    # Save enhanced image
    enhanced_path = output_dir / f"{base_name}_rlt.png"
    cv2.imwrite(str(enhanced_path), output)

    return enhanced_path