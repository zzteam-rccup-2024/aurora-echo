import spacy


def recognize_entities(sentences: str):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(sentences)
    for ent in doc.ents:
        print(ent.text, ent.start_char, ent.end_char, ent.label_)
