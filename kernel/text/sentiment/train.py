from kernel.text.sentiment.model import model, optimizer, criterion
from kernel.text.sentiment.config import epochs
from tqdm import tqdm
from kernel.text.sentiment.datasets import train_iter, test_iter
from kernel.config import device
import torch


def binary_accuracy(preds, y):
    rounded_preds = torch.round(torch.sigmoid(preds))
    correct = (rounded_preds == y).float()
    return correct.sum() / len(correct)


def train():
    model.train()
    for epoch in range(epochs):
        model.train()

        train_loss = 0
        train_acc = 0

        for batch in tqdm(train_iter, desc=f'Epoch {epoch + 1} / {epochs}'):
            text = batch.text.to(device)
            label = batch.label.to(device)

            optimizer.zero_grad()
            output = model(text).squeeze(1)
            loss = criterion(output, label)
            acc = binary_accuracy(output, label)
            loss.backward()
            optimizer.step()

            train_loss += loss.item()
            train_acc += acc.item()
        print(f'Epoch {epoch + 1} / {epochs} - Loss: {train_loss / len(train_iter):.4f} - Acc: {train_acc / len(train_iter):.4f}')

        test_loss = 0
        test_acc = 0
        model.eval()

        with torch.no_grad():
            for batch in tqdm(test_iter):
                text = batch.text.to(device)
                label = batch.label.to(device)

                output = model(text).squeeze(1)
                loss = criterion(output, label)
                acc = binary_accuracy(output, label)

                test_loss += loss.item()
                test_acc += acc.item()
        print(f'Epoch {epoch + 1} / {epochs} - Loss: {test_loss / len(test_iter):.4f} - Acc: {test_acc / len(test_iter):.4f}')

    torch.save(model.state_dict(), 'data/sentiment/model.pth')


def load():
    model.load_state_dict(torch.load('data/sentiment/model.pth'))
