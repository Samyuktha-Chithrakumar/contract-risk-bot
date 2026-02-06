import spacy
from spacy.cli import download

def load_spacy_model():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        download("en_core_web_sm")
        return spacy.load("en_core_web_sm")

nlp = load_spacy_model()


def extract_entities(text):
    doc = nlp(text)

    entities = {
        "Parties": [],
        "Dates": [],
        "Money": [],
        "Locations": []
    }

    for ent in doc.ents:
        if ent.label_ == "ORG":
            entities["Parties"].append(ent.text)
        elif ent.label_ == "DATE":
            entities["Dates"].append(ent.text)
        elif ent.label_ == "MONEY":
            entities["Money"].append(ent.text)
        elif ent.label_ in ["GPE", "LOC"]:
            entities["Locations"].append(ent.text)

    return entities
