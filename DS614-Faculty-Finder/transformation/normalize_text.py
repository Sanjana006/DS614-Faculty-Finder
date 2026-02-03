'''
this module contains functions to normalize and clean text data for faculty profiles.
'''

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
    # remove text in parentheses (e.g. " (On Leave)")
    name = re.sub(r"\(.*?\)", "", name)
    return name.strip().title()

def validate_email(email):
    if isinstance(email, str):
        email = email.strip().lower()
        return email if "@" in email else None
    return None

def specialization_text_to_list(text):
    if not isinstance(text, str):
        return ["not_available"]
    return [a.strip().lower() for a in text.split(",")]
#this function combines bio, research, specialization, and phd_field into a single text block
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
    return "not_available"

import re
import unicodedata

def clean_publication(text: str) -> str:
    if not isinstance(text, str):
        return None

    # Normalize unicode (fixes Â, Ã, etc.)
    text = unicodedata.normalize("NFKD", text)

    # Remove trademark, copyright, registered symbols
    text = re.sub(r"[™®©]", "", text)

    # Remove pound, hash, special currency symbols
    text = re.sub(r"[£€¥₹#]", "", text)

    # Remove LaTeX commands
    text = re.sub(r"\\[a-zA-Z]+(\{.*?\})?", "", text)

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)

    # Remove non-printable & control characters
    text = re.sub(r"[\x00-\x1f\x7f-\x9f]", " ", text)

    # Replace bullets and long dashes
    text = re.sub(r"[•▪–—]", " ", text)

    # Keep only meaningful characters
    text = re.sub(r"[^a-zA-Z0-9.,;:()\- ]", " ", text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text







