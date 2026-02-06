import json, hashlib, datetime, os

LOG_FILE = "audit_logs.json"

def hash_file(content):
    return hashlib.sha256(content.encode()).hexdigest()

def log_event(file_hash, risk_score):
    entry = {
        "timestamp": str(datetime.datetime.utcnow()),
        "file_hash": file_hash,
        "risk_score": risk_score
    }
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump([], f)

    with open(LOG_FILE, "r+") as f:
        data = json.load(f)
        data.append(entry)
        f.seek(0)
        json.dump(data, f, indent=2)
