# Adapt from ResNet-50
import torch
from torchvision.models import resnet50, ResNet50_Weights
import torch.nn as nn
import torch.optim as optim
from kernel.config import device


class FacialModel(nn.Module):
    def __init__(self):
        super(FacialModel, self).__init__()
        self.resnet = resnet50(weights=ResNet50_Weights)
        # Input size to 256 * 256 with RGB channels
        in_features = self.resnet.fc.in_features
        self.resnet.fc = nn.Linear(in_features, 8)

    def forward(self, x):
        return self.resnet(x)


def fetch_model(weights_path: str = None):
    model = FacialModel().to(device)
    if weights_path:
        model.load_state_dict(torch.load(weights_path, map_location=device))

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    return model, criterion, optimizer


def save_model(model, path):
    torch.save(model.state_dict(), path)
