import spacy

nlp: spacy.Language


def load_spacy_model():
    global nlp
    nlp = spacy.load('en_core_web_sm')
