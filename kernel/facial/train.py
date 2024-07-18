from kernel.config import device
import torch
from tqdm import tqdm

epochs = 10


def train_model(model, criterion, optimizer, train_loader, val_loader, save_path):
    for epoch in range(epochs):
        model.train()
        train_loss = 0.0
        for inputs, labels in tqdm(train_loader, desc=f"(Training) Epoch {epoch + 1}/{epochs}"):
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            train_loss += loss.item()

        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for inputs, labels in tqdm(val_loader, desc=f"(Evaluation) Epoch {epoch + 1}/{epochs}"):
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                val_loss += loss.item()

        print(f"Epoch {epoch + 1}/{epochs}.. "
              f"Train loss: {train_loss / len(train_loader):.3f}.. "
              f"Val loss: {val_loss / len(val_loader):.3f}")

    torch.save(model.state_dict(), save_path)
    print("Model saved")
