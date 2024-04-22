from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import pandas as pd

df = pd.read_json("E:/IR/IRProject/Web_Crawler_Sarthak/f1_crawler/f1_records.json")

df = df['paragraphs'].tolist()

tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(df)
cosine_similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)

with open('E:/IR/IRProject/Web_Crawler_Sarthak/f1_crawler/tfidf.pkl', 'wb') as f:
    pickle.dump((tfidf_vectorizer, tfidf_matrix), f)

with open('E:/IR/IRProject/Web_Crawler_Sarthak/f1_crawler/cosine_similarity.pkl', 'wb') as f:
    pickle.dump(cosine_similarities, f)