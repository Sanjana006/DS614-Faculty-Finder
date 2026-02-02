import ast

def _safe_parse_list(text):
    try:
        return ast.literal_eval(text)
    except Exception:
        return []

def build_weighted_corpus(faculty_data):
    """
    Builds a weighted text corpus for each faculty.
    """
    corpus = []

    for faculty in faculty_data:
        specialization = " ".join(
            _safe_parse_list(faculty.get("specialization", ""))
        )
        research = faculty.get("research") or ""
        bio = faculty.get("bio") or ""
        publications = faculty.get("publications") or ""
        phd_field = faculty.get("phd_field") or ""

        document = (
            (specialization + " ") * 3 +
            (research + " ") * 3 +
            (bio + " ") * 2 +
            (phd_field + " ") * 1 +
            (publications + " ") * 1
        )

        corpus.append(document.lower())

    return corpus
