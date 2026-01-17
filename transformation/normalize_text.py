import re 
import pandas as pd

def clean_text(text):
    # remove html tags
    text = re.sub(r"<.*?>", " ", str(text))
    # remove extra spaces
    text = re.sub(r"\s+", " ", text)
    text = text.replace("\n", " ").strip()
    # return lowercase
    return text.lower()

def clean_name(name):
    if not isinstance(name, str):
        return ""
    # remove titles like dr/prog
    name = re.sub(r"\b(dr|prog)\.?\b", "", name, flags=re.IGNORECASE)
    return name.strip().title()

def extract_phd_field(text):
    if not isinstance(text, str):
        return ""
    match = re.search(r"\((.*?)\)", text)
    return match.group(1).strip() if match else text.strip()

def validate_email(email):
    if isinstance(email, str):
        email = email.strip().lower()
        return email if "@" in email else None
    return None

def specialization_text_to_list(text):
    if not isinstance(text, str):
        return []
    return [a.strip().lower() for a in text.split(",")]

def combine_texts(bio, research, specialization, phd_field):
    parts = []
    if isinstance(bio, str):
        parts.append(bio)
    if isinstance(research, str):
        parts.append(research)
    if isinstance(specialization, str):
        parts.append(specialization)
    elif isinstance(specialization, list):
        parts.extend(specialization)
    if isinstance(phd_field, str):
        parts.append(phd_field)
    return " ".join(parts)

def normalize_research(research):
    if isinstance(research, str) and research.strip():
        return clean_text(research).lower()
    return ""

def infer_research_from_other_fields(bio, specialization):
    signals = []
    if isinstance(bio, str):
        signals.append(bio)
    if isinstance(specialization, str):
        signals.append(specialization)
    elif isinstance(specialization, list):
        signals.extend(specialization)
    return clean_text(" ".join(signals)).lower()

def resolved_research(research, bio, specialization):
    normalized_research = normalize_research(research)
    if normalized_research:
        return normalized_research
    return infer_research_from_other_fields(bio, specialization)
