import re

def extract_clauses(text):
    clauses = re.split(r'\n\s*\d+[\.\)]\s+', text)
    clauses = [c.strip() for c in clauses if len(c.strip()) > 30]
    return clauses
