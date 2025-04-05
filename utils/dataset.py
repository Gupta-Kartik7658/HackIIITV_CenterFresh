# utils/dataset.py
import os
import glob
import cv2
from torch.utils.data import Dataset
import torch
import numpy as np

class CustomESRGANDataset(Dataset):
    def __init__(self, lr_dir, hr_dir):
        super().__init__()
        self.lr_images = sorted(glob.glob(os.path.join(lr_dir, '*')))
        self.hr_images = sorted(glob.glob(os.path.join(hr_dir, '*')))

    def __getitem__(self, index):
        lr = cv2.imread(self.lr_images[index], cv2.IMREAD_COLOR)
        hr = cv2.imread(self.hr_images[index], cv2.IMREAD_COLOR)

        # Convert to tensor
        lr = torch.from_numpy(np.transpose(lr, (2, 0, 1))).float() / 255.
        hr = torch.from_numpy(np.transpose(hr, (2, 0, 1))).float() / 255.

        return {'LR': lr, 'HR': hr}

    def __len__(self):
        return len(self.lr_images)
