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

def clean_publications(text):
    """
    Cleans and normalizes publication text into a structured list of publications.
    """
    if not isinstance(text, str) or not text.strip():
        return []

    # 1. Remove HTML tags
    text = re.sub(r"<.*?>", " ", text)

    # 2. Normalize separators (•, |, ;, newline → ||)
    text = re.sub(r"[•|;\n]+", "||", text)

    # 3. Remove URLs and DOIs
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"\bdoi:\S+", "", text, flags=re.IGNORECASE)

    # 4. Remove excessive punctuation
    text = re.sub(r"[^\w\s(),.-]", " ", text)

    # 5. Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # 6. Split into individual publications
    publications = [p.strip() for p in text.split("||") if len(p.strip()) > 20]

    cleaned_publications = []
    seen = set()

    for pub in publications:
        pub_lower = pub.lower()

        # 7. Remove year-only or noise entries
        if re.fullmatch(r"\(?\d{4}\)?", pub_lower):
            continue

        # 8. De-duplicate using normalized signature
        signature = re.sub(r"\d{4}", "", pub_lower)
        signature = re.sub(r"\W+", "", signature)

        if signature not in seen:
            seen.add(signature)
            cleaned_publications.append(pub)

    return cleaned_publications

def extract_paper_topics(citation_list):
    topics = []
    for citation in citation_list:
        # Split by commas first (authors are usually before the first comma)
        parts = citation.split(",")
        
        if len(parts) > 1:
            # The topic usually starts after the author list
            # Find the segment that looks like a title (before journal names like Springer, IEEE, etc.)
            for segment in parts[1:]:
                seg = segment.strip()
                # Heuristic: skip if segment contains journal/publisher keywords
                if not re.search(r"(Springer|IEEE|IETE|Journal|World Scientific|Taylor Francis|Circuits|Devices|Systems|Review|Processing)", seg, re.I):
                    topics.append(seg)
                    break
        else:
            topics.append(citation.strip())
    return topics



