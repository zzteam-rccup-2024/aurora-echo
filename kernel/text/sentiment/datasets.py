# Uses IMDB dataset from torchtext.datasets
import torch
from torchtext import data, datasets
import spacy

TEXT = None
LABEL = None
train_iter = None
test_iter = None
eval_iter = None
INPUT_DIM = 25002
BATCH_SIZE = 16
EMBEDDING_DIM = 100
HIDDEN_DIM = 256
OUTPUT_DIM = 1
N_LAYERS = 2
BIDIRECTIONAL = True
DROPOUT = 0.5
nlp = spacy.load('en_core_web_sm')


def build_embedded():
    global TEXT, LABEL, train_iter, test_iter, eval_iter, INPUT_DIM, BATCH_SIZE, EMBEDDING_DIM, HIDDEN_DIM, OUTPUT_DIM, N_LAYERS, BIDIRECTIONAL, DROPOUT
    print('Loading spaCy embedding layer...')

    TEXT = data.Field(tokenize=lambda x: [tok.text for tok in nlp.tokenizer(x)], lower=True)
    LABEL = data.LabelField(dtype=torch.float)

    dataset = datasets.IMDB.splits(TEXT, LABEL)[0]

    train_set, test_set = dataset.split()

    print('Building vocabulary...')

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
