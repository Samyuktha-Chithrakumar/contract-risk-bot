# GenAI-Powered Contract Analysis & Risk Assessment Bot

## Overview
This project is a GenAI-powered legal assistant designed to help Indian Small and Medium Enterprises (SMEs understand complex contracts, identify potential risks, and make informed business decisions. Contracts often contain legal language that is difficult for non-legal professionals to understand. This application simplifies that process by automatically analyzing contracts and explaining them in clear, business-friendly language.

The system works with employment agreements, vendor contracts, lease agreements, partnership deeds, and service contracts.

---

## Key Features

### Contract Upload
- Supports PDF (text-based), DOC/DOCX, and TXT files
- No contract data is stored permanently

### Contract Understanding
- Automatically detects the contract type
- Splits the document into individual clauses
- Extracts key entities such as parties, dates, amounts, and locations

### Risk Analysis
- Assigns risk levels (Low / Medium / High) to each clause
- Calculates an overall contract risk score
- Flags high-risk clauses such as:
  - Unilateral termination
  - Penalty and indemnity clauses
  - Non-compete restrictions
  - Auto-renewal and lock-in periods

### Plain English Explanation
- Each clause is explained in simple business English
- Highlights why a clause may be risky
- Suggests safer renegotiation alternatives for SMEs

### Advanced Legal NLP
- Classifies clauses as obligations, rights, or prohibitions
- Detects ambiguous terms like “reasonable” or “best efforts”
- Matches clauses with SME-friendly standard templates using sentence similarity

### Multilingual Support
- Detects English and Hindi contracts
- Internally normalizes content for analysis
- Outputs explanations in simple English

### Reports & Audit
- Generates downloadable PDF risk reports with timestamps
- Maintains local audit logs using file hashes (no raw contract storage)

---

## Technology Stack

- **Frontend/UI:** Streamlit  
- **NLP:** Python, spaCy, NLTK  
- **Clause Similarity:** Sentence Transformers  
- **LLM Reasoning:** Architecture supports GPT-4 or Claude-3  
- **Storage:** Local files and JSON logs only  

---

## How It Solves the Problem

SMEs often sign contracts without fully understanding hidden risks due to legal complexity and lack of access to legal experts. This system:
- Makes contracts readable and understandable
- Identifies risky clauses before signing
- Provides actionable suggestions without legal jargon
- Ensures privacy by avoiding external data storage
- Reduces dependency on costly legal consultations

---

## Running the Application

```bash
Download python 3.11
## Steps to Run this app

python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m spacy download en_core_web_sm
set OPENAI_API_KEY=your_secret_key_here
streamlit run app.py
