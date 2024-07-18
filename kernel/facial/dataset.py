from torchvision.datasets import ImageFolder
from kernel.facial.transform import transform
from torch.utils.data import random_split, DataLoader
from kernel.facial.config import batch_size


def load_data_loader():
    dataset = ImageFolder(root='data/datasets/emotional', transform=transform)

    train_size = int(0.81 * len(dataset))
    test_size = len(dataset) - train_size

    train_dataset, test_dataset = random_split(dataset, [train_size, test_size])

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    return train_loader, test_loader
