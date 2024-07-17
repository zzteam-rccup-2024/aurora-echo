# Uses IMDB dataset from torchtext.datasets
import torch
from torch.utils.data import random_split
from torchtext import data, datasets
import spacy

nlp = spacy.load('en_core_web_sm')

TEXT = data.Field(tokenize=lambda x: [tok.text for tok in nlp.tokenizer(x)], lower=True)
LABEL = data.LabelField(dtype = torch.float)

dataset = datasets.IMDB.splits(TEXT, LABEL)[0]

train_set, test_set = dataset.split()

TEXT.build_vocab(train_set, max_size=25000)
LABEL.build_vocab(train_set)

train_iter, test_iter, eval_iter = data.BucketIterator.splits(
    (train_set, test_set, test_set),
    batch_size=64,
    device=torch.device('cuda' if torch.cuda.is_available() else 'cpu')
)

INPUT_DIM = len(TEXT.vocab)
BATCH_SIZE = 16
EMBEDDING_DIM = 100
HIDDEN_DIM = 256
OUTPUT_DIM = 1
N_LAYERS = 2
BIDIRECTIONAL = True
DROPOUT = 0.5
