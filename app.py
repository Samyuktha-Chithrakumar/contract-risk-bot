import streamlit as st
from datetime import datetime


# ---------- Utils ----------
from utils.pdf_reader import extract_pdf_text
from utils.docx_reader import extract_docx_text
from utils.logger import hash_file, log_event
from utils.pdf_exporter import export_pdf

# ---------- NLP ----------
from nlp.clause_extractor import extract_clauses
from nlp.ner import extract_entities
from nlp.contract_classifier import classify_contract
from nlp.obligation_classifier import classify_clause_type
from nlp.ambiguity_detector import detect_ambiguity
from nlp.risk_engine import score_clause, overall_risk
from nlp.similarity import find_similar_clause
from nlp.parser import detect_language

# ---------- LLM (Demo Mode / Fallback) ----------
from llm.analyzer import analyze_clause

if "report_count" not in st.session_state:
    st.session_state.report_count = 0

# ---------- UI CONFIG ----------
st.set_page_config(page_title="GenAI Contract Risk Assistant", layout="wide")
st.title("📄 GenAI-Powered Contract Analysis & Risk Assessment Bot")
#st.caption("🧪 Demo Mode Enabled | Designed for Indian SMEs")

# ======================================================
# A. FILE UPLOAD
# ======================================================
uploaded_file = st.file_uploader(
    "Upload Contract (PDF / DOCX / TXT)",
    type=["pdf", "docx", "txt"]
)

if uploaded_file:

    # ======================================================
    # B. TEXT EXTRACTION
    # ======================================================
    if uploaded_file.type == "application/pdf":
        text = extract_pdf_text(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        text = extract_docx_text(uploaded_file)
    else:
        text = uploaded_file.read().decode("utf-8")

    # ======================================================
    # C. LANGUAGE DETECTION (English / Hindi)
    # ======================================================
    lang = detect_language(text)
    if lang == "hi":
        st.warning("Hindi contract detected. (Demo: internally normalized to English)")

    # ======================================================
    # D. CONTRACT TYPE CLASSIFICATION
    # ======================================================
    contract_type = classify_contract(text)
    st.info(f"📑 Contract Type Detected: **{contract_type}**")

    # ======================================================
    # E. ENTITY EXTRACTION
    # ======================================================
    st.subheader("🔍 Key Entities Identified")
    entities = extract_entities(text)
    st.json(entities)

    # ======================================================
    # F. CLAUSE EXTRACTION
    # ======================================================
    clauses = extract_clauses(text)

    st.subheader("📜 Clause-by-Clause Analysis")

    clause_risks = []
    report_lines = []

    for idx, clause in enumerate(clauses[:10]):  # limit for demo
        risk = score_clause(clause)
        clause_risks.append(risk)

        clause_type = classify_clause_type(clause)
        ambiguities = detect_ambiguity(clause)
        similar_clause, similarity_score = find_similar_clause(clause)

        with st.expander(f"Clause {idx + 1} | Risk: {risk}"):
            st.markdown("**Clause Text:**")
            st.write(clause)

            # ------------------------------
            # Obligation / Right / Prohibition
            # ------------------------------
            st.caption(f"📌 Clause Type: **{clause_type}**")

            # ------------------------------
            # Ambiguity Detection
            # ------------------------------
            if ambiguities:
                st.warning(f"⚠️ Ambiguous terms detected: {', '.join(ambiguities)}")

            # ------------------------------
            # AI / Demo Explanation
            # ------------------------------
            explanation = analyze_clause(clause)
            st.markdown("### 🧠 Plain English Explanation")
            st.write(explanation)

            # ------------------------------
            # Clause Similarity
            # ------------------------------
            if similarity_score > 0.75:
                st.info(f"✅ Similar SME-friendly clause found (Similarity: {similarity_score})")
                st.write(similar_clause)

            report_lines.append(
                f"Clause {idx + 1} | Risk: {risk}\n{explanation}\n"
            )

    # ======================================================
    # G. OVERALL RISK ASSESSMENT
    # ======================================================
    overall = overall_risk(clause_risks)
    st.success(f"🚨 Overall Contract Risk: **{overall}**")

    # ======================================================
    # H. AUDIT LOGGING (NO RAW TEXT STORED)
    # ======================================================
    file_hash = hash_file(text)
    log_event(file_hash, overall)

    # ======================================================
    # I. PDF EXPORT
    # ======================================================
    if st.button("📄 Download Risk Summary (PDF)"):
        st.session_state.report_count += 1

        # Timestamp for filename
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        filename = (
            f"contract_report_{timestamp}_"
            f"{st.session_state.report_count}.pdf"
        )

        summary_text = (
            f"Contract Type: {contract_type}\n"
            f"Overall Risk: {overall}\n\n"
        )
        summary_text += "\n".join(report_lines)

        pdf_file = export_pdf(summary_text, filename)
        st.success(f"PDF generated: {pdf_file}")


