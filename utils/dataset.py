# utils/dataset.py
import os
import glob
import cv2
from torch.utils.data import Dataset
import torch
import numpy as np

class ImageDataset(Dataset):
    def __init__(self, image_dir):
        super().__init__()
        self.images = sorted(glob.glob(os.path.join(image_dir, '*')))

    def __getitem__(self, index):
        img = cv2.imread(self.images[index], cv2.IMREAD_COLOR)
        
        # Convert to tensor
        img = torch.from_numpy(np.transpose(img, (2, 0, 1))).float() / 255.
        
        return {'image': img}

    def __len__(self):
        return len(self.images)
