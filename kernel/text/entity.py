import spacy


def recognize_entities(sentences: str) -> list[tuple[str, str]]:
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(sentences)
    result = []
    for ent in doc.ents:
        result.append((ent.text, ent.label_))
    return result
