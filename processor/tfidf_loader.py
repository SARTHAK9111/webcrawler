import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_data(tfidf_index_file, cosine_similarities_file):
    # Load TF-IDF vectorizer and matrix
    with open(tfidf_index_file, 'rb') as f:
        tfidf_vectorizer, tfidf_matrix = pickle.load(f)

    # Load cosine similarities
    with open(cosine_similarities_file, 'rb') as f:
        cosine_similarities = pickle.load(f)

    return tfidf_vectorizer, tfidf_matrix, cosine_similarities

def search(query, tfidf_vectorizer, tfidf_matrix, cosine_similarities, documents, top_k):
    # Vectorize query
    query_vector = tfidf_vectorizer.transform([query])

    # Calculate cosine similarity of query with all documents
    query_cosine_similarities = cosine_similarity(query_vector, tfidf_matrix)

    # Get indices of most similar documents
    most_similar_indices = query_cosine_similarities.argsort()[0][::-1]

    # Display most similar documents
    results = []
    for idx in most_similar_indices[:top_k]:
        similarity_score = query_cosine_similarities[0][idx]
        document = documents.iloc[idx]['title'].strip()
        results.append((similarity_score, document))

    return results

def search_query(query):
    tfidf_index_file = 'E:/IR/IRProject/Web_Crawler_Sarthak/f1_crawler/tfidf.pkl'
    cosine_similarities_file = 'E:/IR/IRProject/Web_Crawler_Sarthak/f1_crawler/cosine_similarity.pkl'
    file_path = 'E:/IR/IRProject/Web_Crawler_Sarthak/f1_crawler/f1_records.json'

    # Load indexed data
    tfidf_vectorizer, tfidf_matrix, cosine_similarities = load_data(
        tfidf_index_file, cosine_similarities_file)

    # Load documents from CSV
    df_documents = pd.read_json(file_path)

    # Example: Perform search
    results = search(query, tfidf_vectorizer, tfidf_matrix, cosine_similarities, df_documents, top_k=5)

    return results