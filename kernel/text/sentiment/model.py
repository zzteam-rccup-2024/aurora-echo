import gc
import torch.nn as nn
import torch
from kernel.config import device


class SentimentRNN(nn.Module):
    def __init__(self, train=False):
        if train:
            from kernel.text.sentiment.datasets import build_embedded
            build_embedded()
        from kernel.text.sentiment.datasets import INPUT_DIM, EMBEDDING_DIM, HIDDEN_DIM, OUTPUT_DIM, N_LAYERS, \
            BIDIRECTIONAL, DROPOUT
        super().__init__()
        self.embedding = nn.Embedding(INPUT_DIM, EMBEDDING_DIM)
        self.rnn = nn.LSTM(EMBEDDING_DIM, HIDDEN_DIM, num_layers=N_LAYERS, bidirectional=BIDIRECTIONAL, dropout=DROPOUT)
        self.fc = nn.Linear(HIDDEN_DIM * 2 if BIDIRECTIONAL else HIDDEN_DIM, OUTPUT_DIM)
        self.dropout = nn.Dropout(DROPOUT)

    def forward(self, text):
        embedded = self.dropout(self.embedding(text))
        output, (hidden, cell) = self.rnn(embedded)
        hidden = self.dropout(torch.cat((hidden[-2, :, :], hidden[-1, :, :]), dim=1))
        return self.fc(hidden)


model = SentimentRNN(train=False).to(device=device)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
criterion = nn.CrossEntropyLoss()


def release_model():
    del model
    del optimizer
    del criterion
    gc.collect()
