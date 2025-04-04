# finetune.py
import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from utils.dataset import CustomESRGANDataset
import RRDBNet_arch as arch

# Paths
pretrained_path = 'models/RRDB_ESRGAN_x4.pth'
lr_path = 'dataset/LR'
hr_path = 'dataset/HR'
save_path = 'models/finetuned_ESRGAN.pth'

# Hyperparameters
batch_size = 4
num_epochs = 10
lr = 1e-5

# Load dataset
dataset = CustomESRGANDataset(lr_path, hr_path)
dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

# Load model
model = arch.RRDBNet(3, 3, 64, 23, gc=32)
model.load_state_dict(torch.load(pretrained_path), strict=True)
model.train()

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

# Loss + Optimizer
criterion = nn.L1Loss()  # Simple pixel-wise loss
optimizer = optim.Adam(model.parameters(), lr=lr)

# Training Loop
for epoch in range(num_epochs):
    for i, data in enumerate(dataloader):
        lr_img = data['LR'].to(device)
        hr_img = data['HR'].to(device)

        sr_img = model(lr_img)
        loss = criterion(sr_img, hr_img)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if i % 10 == 0:
            print(f"[Epoch {epoch+1}/{num_epochs}] Step {i} Loss: {loss.item():.4f}")

# Save the fine-tuned model
torch.save(model.state_dict(), save_path)
print(f"✅ Model fine-tuned and saved at {save_path}")
