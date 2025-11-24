# normalizer.py

"""
Lightweight Indic code-mix normalizer for SahaYaa.

Cleans fillers, common banking slang, simple Hinglish, and prepares text for intent models.
"""

import regex as re
from unidecode import unidecode


# Base / cross-language fillers

CORE_FILLERS = {
    "yaar", "bhai", "bhaiya", "acha", "accha", "haan", "na",
    "toh", "matlab", "umm", "uh", "arey", "arre", "please", "plz",
    "zara", "jara", "thoda", "thodi",
}


# Language-specific fillers

HINDI_FILLERS = {
    "matlab", "aisa", "waise", "accha", "acha",
    "yaar", "toh", "na", "zara", "thoda", "thodi",
    "bas", "chalo", "dekho",
}

ENGLISH_FILLERS = {
    "um", "uh", "well", "like", "you know",
    "actually", "basically", "just", "so",
    "anyway", "i mean", "only", "kinda", "sorta",
}

TAMIL_FILLERS = {
    "da", "pa", "ma", "machan", "macchi",
    "seri", "ille", "illeya", "enna", "appadi",
    "konjam",
}

TELUGU_FILLERS = {
    "ra", "amma", "ayya", "asalu", "kada",
    "ante", "le", "anna", "ayya", "arey",
    "koncham",
}

BENGALI_FILLERS = {
    "na", "to", "bolchi", "mane", "jeno", "eta", "oi", "accha",
}

ALL_FILLERS = (
    CORE_FILLERS
    | HINDI_FILLERS
    | ENGLISH_FILLERS
    | TAMIL_FILLERS
    | TELUGU_FILLERS
    | BENGALI_FILLERS
)


# Romanized Hindi + banking slang

ROMAN_HI_MAP = {
    "mera": "mera",
    "meri": "meri",
    "account": "account",
    "akaunt": "account",

    "bal": "balance",
    "balance": "balance",
    "batao": "batao",
    "bata": "batao",
    "bataao": "batao",

    "bhej": "bhej",
    "bhejo": "bhejo",

    "paise": "paise",
    "paisa": "paisa",

    "upi": "upi",
    "transfer": "transfer",

    "loan": "loan",
    "emi": "emi",
    "bill": "bill",
    "recharge": "recharge",
}

BANKING_SYNONYMS = {
    "bal": "balance",
    "txn": "transaction",
    "txns": "transactions",
    "xfer": "transfer",
    "paytm": "wallet",
    "gpay": "upi",
    "phonepe": "upi",
}


# Token helpers

def _tokenize(text: str):
    """
    Split text into simple word and punctuation tokens.
    """
    text = re.sub(r"([,.!?])", r" \1 ", text)
    tokens = text.split()
    return tokens


def _is_latin(word: str) -> bool:
    """
    True if token is mainly Latin script (likely romanized).
    """
    w = unidecode(word)
    return bool(re.fullmatch(r"[A-Za-z]+", w))


# Filler detection

def is_filler_token(token: str) -> bool:
    """
    Decide if a token is just conversational filler.
    """
    raw = token.strip().lower()
    if not raw:
        return False

    if re.match(r"^ना.*रा$", raw) and len(raw) <= 5:
        return True

    roman = unidecode(raw).lower()

    if raw in ALL_FILLERS or roman in ALL_FILLERS:
        return True

    if roman in {"na", "naa", "naaa"}:
        return True

    if roman.startswith("na") and len(roman) <= 7:
        if any(sub in roman for sub in ["zra", "zara", "jra", "sra"]):
            return True

    return False


# Main normalizer

def normalize_text(text: str) -> str:
    """
    Clean code-mixed ASR text: drop fillers, map slang, and tidy spacing.
    """
    text = text.strip().lower()

    text = re.sub(r"[“”\"]", "\"", text)
    text = re.sub(r"[’‘']", "'", text)

    tokens = _tokenize(text)
    normalized_tokens = []

    for tok in tokens:
        base = tok

        if is_filler_token(base):
            continue

        leading_punct = ""
        trailing_punct = ""

        m_lead = re.match(r"^([,.!?]+)(.+)$", base)
        if m_lead:
            leading_punct, base = m_lead.group(1), m_lead.group(2)

        m_trail = re.match(r"^(.+?)([,.!?]+)$", base)
        if m_trail:
            base, trailing_punct = m_trail.group(1), m_trail.group(2)

        if base in BANKING_SYNONYMS:
            base = BANKING_SYNONYMS[base]

        if _is_latin(base) and base in ROMAN_HI_MAP:
            base = ROMAN_HI_MAP[base]

        token_final = leading_punct + base + trailing_punct

        if token_final.strip():
            normalized_tokens.append(token_final)

    cleaned = " ".join(normalized_tokens)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


# Quick manual check

if __name__ == "__main__":
    examples = [
        "Acha yaar mera account ka bal batao na zara",
        "Bhaiya UPI se 500 Riya ko bhej do please",
        "Regular wala recharge kar do konjam",
        "Loan ka balance batao, EMI kab due hai?",
        "Can you just show my last five UPI transactions, please?",
    ]

    for s in examples:
        print("\nRAW: ", s)
        print("NORM:", normalize_text(s))
