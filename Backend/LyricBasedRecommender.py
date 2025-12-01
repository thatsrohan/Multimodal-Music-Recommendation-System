#!/usr/bin/env python
# coding: utf-8

"""
Music Recommendation System (Lyric-based)
-----------------------------------------
This script builds a simple content-based recommender using song lyrics.
It uses TF-IDF + Cosine Similarity to suggest similar songs based on text.
"""

# =========================================================
# 1. Import libraries
# =========================================================
import pandas as pd
import nltk
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# =========================================================
# 2. Load dataset
# =========================================================
df = pd.read_csv(r"D:\Workspace\Multimodal-Music-Recommender-2nd-Iteration\datasets\spotify_millsongdata.csv")

print("Dataset shape before sampling:", df.shape)

# Sample to reduce size (optional)
df = df.sample(5000).drop('link', axis=1).reset_index(drop=True)
print("Dataset shape after sampling:", df.shape)

# =========================================================
# 3. Preprocessing
# =========================================================
# Handle missing values
print("Null values per column:\n", df.isnull().sum())

# Lowercase, remove unwanted chars/newlines
df['text'] = df['text'].str.lower().replace(r'^\w\s', ' ', regex=True).replace(r'\n', ' ', regex=True)

# =========================================================
# 4. Tokenization + Stemming
# =========================================================
stemmer = PorterStemmer()

def tokenization(txt):
    tokens = nltk.word_tokenize(txt)
    stemming = [stemmer.stem(w) for w in tokens]
    return " ".join(stemming)

# Apply tokenization
df['text'] = df['text'].apply(tokenization)

# =========================================================
# 5. Vectorization (TF-IDF)
# =========================================================
tfidvector = TfidfVectorizer(analyzer='word', stop_words='english')
matrix = tfidvector.fit_transform(df['text'])

# Compute similarity matrix
similarity = cosine_similarity(matrix)

# =========================================================
# 6. Recommendation Function
# =========================================================
def recommendations(song_name_or_lyrics):
    """
    Recommends top 20 similar songs based on:
    - exact song title match (preferred)
    - OR lyrics snippet (fallback)
    """

    # Try exact song name match
    match = df[df['song'].str.lower() == song_name_or_lyrics.lower()]

    if not match.empty:
        idx = match.index[0]
    else:
        # Fallback: treat input as lyrics → vectorize & find closest match
        input_vec = tfidvector.transform([tokenization(song_name_or_lyrics)])
        sims = cosine_similarity(input_vec, matrix).flatten()

        idx = sims.argmax()

    # Sort all songs by similarity
    distances = sorted(
        list(enumerate(similarity[idx])),
        reverse=True,
        key=lambda x: x[1]
    )

    # Prepare top 20 results (excluding itself)
    recommended_rows = []
    for m_id, score in distances[1:21]:
        row = df.iloc[m_id]
        recommended_rows.append({
            "artist": row["artist"],
            "song": row["song"],
            "text": row["text"]
        })

    return pd.DataFrame(recommended_rows)

    


