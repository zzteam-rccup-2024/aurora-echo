# Adapt from ResNet-50
import torch
from torchvision.models import googlenet, GoogLeNet_Weights
import torch.nn as nn
import torch.optim as optim
from kernel.config import device


class FacialModel(nn.Module):
    def __init__(self):
        super(FacialModel, self).__init__()
        self.net = googlenet(weights=GoogLeNet_Weights)
        # Input size to 256 * 256 with RGB channels
        in_features = self.net.fc.in_features
        self.net.fc = nn.Linear(in_features, 8)

    def forward(self, x):
        return self.net(x)


def fetch_model(weights_path: str = None):
    model = FacialModel().to(device)
    if weights_path:
        model.load_state_dict(torch.load(weights_path, map_location=device))

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    return model, criterion, optimizer


def save_model(model, path):
    torch.save(model.state_dict(), path)
