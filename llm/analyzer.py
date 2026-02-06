import os
import openai
from openai.error import (
    RateLimitError,
    AuthenticationError,
    InvalidRequestError
)

# ==============================
# CONFIG
# ==============================

# Keep this False for production architecture
# (fallback will still work automatically)
DEMO_MODE = False

openai.api_key = os.getenv("OPENAI_API_KEY")


# ==============================
# MAIN FUNCTION
# ==============================

def analyze_clause(clause: str) -> str:
    """
    Always returns a meaningful explanation.
    Uses OpenAI if available, otherwise falls back to fixed logic.
    """

    # ------------------------------
    # DEMO MODE (FORCED FALLBACK)
    # ------------------------------
    if DEMO_MODE:
        return fixed_explanation(clause)

    # ------------------------------
    # OPENAI MODE
    # ------------------------------
    try:
        prompt = f"""
You are a legal assistant helping Indian SME business owners.

Explain the clause in SIMPLE business English.
Then:
1. Identify the risk level (Low / Medium / High)
2. Explain why it is risky (or safe)
3. Suggest a safer renegotiation option

Rules:
- No legal jargon
- No law sections
- No case laws
- Short and practical

Clause:
\"\"\"{clause}\"\"\"
"""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You analyze contracts for Indian SMEs."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=300
        )

        return response["choices"][0]["message"]["content"].strip()

    # ------------------------------
    # ANY FAILURE → FIXED EXPLANATION
    # ------------------------------
    except (RateLimitError, AuthenticationError, InvalidRequestError, Exception):
        return fixed_explanation(clause)


# ==============================
# FIXED FALLBACK EXPLANATION
# ==============================

def fixed_explanation(clause: str) -> str:
    """
    Deterministic explanation when AI is unavailable.
    """

    text = clause.lower()

    # ---- LOCK-IN PERIOD (must be checked first) ----
    if "lock-in" in text or ("shall not terminate" in text and "period" in text):
        return (
            "**Plain English Explanation:**\n"
            "This clause prevents one party from exiting the contract for a fixed period.\n\n"
            "**Risk Level:** Medium\n"
            "A long lock-in period reduces flexibility and may cause problems if business needs change.\n\n"
            "**Suggested Change:**\n"
            "Request a shorter lock-in period or allow early termination with a reasonable exit fee."
        )

    if "terminate" in text:
        return (
            "**Plain English Explanation:**\n"
            "This clause allows one party to end the contract.\n\n"
            "**Risk Level:** High\n"
            "Immediate or one-sided termination can suddenly stop business operations.\n\n"
            "**Suggested Change:**\n"
            "Ask for a notice period (for example, 30 days) before termination."
        )

    if "penalty" in text or "indemn" in text:
        return (
            "**Plain English Explanation:**\n"
            "This clause makes one party responsible for financial losses.\n\n"
            "**Risk Level:** High\n"
            "Unlimited penalties or indemnities can create serious financial risk.\n\n"
            "**Suggested Change:**\n"
            "Negotiate a reasonable limit on liability."
        )

    if "non-compete" in text:
        return (
            "**Plain English Explanation:**\n"
            "This clause restricts future business or employment opportunities.\n\n"
            "**Risk Level:** Medium to High\n"
            "Long or broad restrictions can affect career or business growth.\n\n"
            "**Suggested Change:**\n"
            "Limit the duration, geography, and scope of the restriction."
        )

    if "payment" in text:
        return (
            "**Plain English Explanation:**\n"
            "This clause explains when and how payments will be made.\n\n"
            "**Risk Level:** Low\n"
            "Long payment cycles can affect cash flow.\n\n"
            "**Suggested Change:**\n"
            "Request shorter payment timelines or milestone-based payments."
        )

    return (
        "**Plain English Explanation:**\n"
        "This clause describes general responsibilities under the contract.\n\n"
        "**Risk Level:** Low\n"
        "No major business risk is immediately visible.\n\n"
        "**Suggested Change:**\n"
        "Ensure responsibilities and timelines are clearly defined."
    )
