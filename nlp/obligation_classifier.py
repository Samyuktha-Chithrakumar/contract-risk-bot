def classify_clause_type(clause):
    c = clause.lower()

    if any(x in c for x in ["shall", "must", "is required to"]):
        return "Obligation"
    if any(x in c for x in ["may", "is entitled to"]):
        return "Right"
    if any(x in c for x in ["shall not", "must not", "is prohibited"]):
        return "Prohibition"

    return "Neutral"
