from sklearn.feature_extraction.text import TfidfVectorizer

def train_vectorizer(corpus):
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.9,
        sublinear_tf=True
    )
    matrix = vectorizer.fit_transform(corpus)
    return vectorizer, matrix
