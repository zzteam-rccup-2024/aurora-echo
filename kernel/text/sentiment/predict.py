from kernel.text.sentiment.datasets import TEXT
from kernel.config import device
import torch


def predict_sentiment(model, sentence, nlp, min_len=5):
    model.eval()
    tokens = [tok.text for tok in nlp(sentence)]
    if len(tokens) < min_len:
        tokens += ['<pad>'] * (min_len - len(tokens))
    indexed = [TEXT.vocab.stoi[t] for t in tokens]
    tensor = torch.LongTensor(indexed).to(device)
    tensor = tensor.unsqueeze(1)
    prediction = torch.sigmoid(model(tensor))
    return prediction.item()
