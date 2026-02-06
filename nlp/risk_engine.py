RISK_KEYWORDS = {
    "High": [
        "terminate immediately",
        "without notice",
        "penalty",
        "indemnify",
        "non-compete"
    ],
    "Medium": [
        "auto-renew",
        "exclusive",
        "arbitration"
    ]
}


def score_clause(clause):
    clause_lower = clause.lower()
    for risk, words in RISK_KEYWORDS.items():
        if any(w in clause_lower for w in words):
            return risk
    return "Low"

def overall_risk(scores):
    if "High" in scores:
        return "High"
    if "Medium" in scores:
        return "Medium"
    return "Low"
