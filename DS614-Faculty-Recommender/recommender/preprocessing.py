import re

def load_stopwords(path="data/stopwords.txt"):
    with open(path) as f:
        return set(w.strip() for w in f)

STOPWORDS = load_stopwords()

PHRASES = [
    "computer vision",
    "machine learning",
    "data science",
    "deep learning",
    "natural language processing"
]

def merge_phrases(text):
    text = text.lower()
    for p in PHRASES:
        text = text.replace(p, p.replace(" ", "_"))
    return text

def preprocess(text):
    text = merge_phrases(text.lower())
    text = re.sub(r'[^a-z_ ]', ' ', text)
    tokens = text.split()
    tokens = [t for t in tokens if t not in STOPWORDS and len(t) > 2]
    return tokens
