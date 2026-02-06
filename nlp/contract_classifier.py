def classify_contract(text):
    text = text.lower()

    if "employee" in text or "employment" in text:
        return "Employment Agreement"
    if "lease" in text or "rent" in text:
        return "Lease Agreement"
    if "vendor" in text or "supplier" in text:
        return "Vendor Agreement"
    if "partner" in text or "partnership" in text:
        return "Partnership Deed"
    if "service" in text or "services" in text:
        return "Service Agreement"

    return "General Commercial Contract"
