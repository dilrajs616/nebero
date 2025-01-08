from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
import string
from nltk.corpus import stopwords

import nltk
nltk.download('stopwords')

def preprocess_text(text):
    text = text.lower()

    text = ''.join([char for char in text if char not in string.punctuation])

    stop_words = set(stopwords.words("english"))
    text = ' '.join([word for word in text.split() if word not in stop_words])

    return text

def extract_keywords_from_document(doc, num_keywords=10):
    preprocessed_doc = preprocess_text(doc)

    vectorizer = TfidfVectorizer(max_features=1000)
    tfidf_matrix = vectorizer.fit_transform([preprocessed_doc])

    tfidf_matrix = normalize(tfidf_matrix, axis=0)

    feature_names = vectorizer.get_feature_names_out()

    tfidf_scores = zip(feature_names, tfidf_matrix.toarray()[0])

    sorted_keywords = sorted(tfidf_scores, key=lambda x: x[1], reverse=True)

    top_keywords = [keyword for keyword, score in sorted_keywords[:num_keywords]]

    return top_keywords

def extract_keywords(documents, num_keywords=10):
    all_keywords = []

    for doc in documents:
        doc_keywords = extract_keywords_from_document(doc, num_keywords)
        all_keywords.extend(doc_keywords)

    unique_keywords = list(set(all_keywords))

    return unique_keywords

