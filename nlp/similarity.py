from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json

model = SentenceTransformer("all-MiniLM-L6-v2")

with open("templates/standard_clauses.json") as f:
    STANDARD = json.load(f)

def find_similar_clause(clause):
    clause_emb = model.encode([clause])
    best_match = None
    best_score = 0

    for name, std_clause in STANDARD.items():
        std_emb = model.encode([std_clause])
        score = cosine_similarity(clause_emb, std_emb)[0][0]

        if score > best_score:
            best_score = score
            best_match = std_clause

    return best_match, round(best_score, 2)
