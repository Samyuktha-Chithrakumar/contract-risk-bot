AMBIGUOUS_TERMS = [
    "reasonable",
    "as applicable",
    "from time to time",
    "as required",
    "best efforts"
]

def detect_ambiguity(clause):
    found = [term for term in AMBIGUOUS_TERMS if term in clause.lower()]
    return found
