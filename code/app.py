from flask import Flask, request, jsonify, render_template
import numpy as np
import pandas as pd
import pickle
import re
import logging
# from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load Netflix dataset
try:
    netflix_data = pd.read_csv("movie_data.csv")
    logging.info("Netflix dataset loaded successfully")
except Exception as e:
    logging.error(f"Error loading Netflix dataset: {str(e)}")

# Load precomputed TF-IDF matrix and cosine similarity matrix
try:
    tfidf_matrix = np.load('tfid_matrix.npy', allow_pickle=True)
    cosine_sim = np.load('cosine_sim_matrix.npy', allow_pickle=True)
    with open('tfidf_vectorizer.pkl', 'rb') as f:
        tfidf_vectorizer = pickle.load(f)
    logging.info("TF-IDF matrix, cosine similarity matrix, and vectorizer loaded successfully")
except Exception as e:
    logging.error(f"Error loading TF-IDF matrix, cosine similarity matrix, or vectorizer: {str(e)}")

class FlixHub:
    def __init__(self, df, cosine_sim):
        self.df = df
        self.cosine_sim = cosine_sim
    
    def recommendation(self, title, total_result=5, threshold=0.5):
        idx = self.find_id(title)
        self.df['similarity'] = self.cosine_sim[idx]
        sort_df = self.df.sort_values(by='similarity', ascending=False)[1:total_result + 1]
        
        movies = sort_df['title'][sort_df['type'] == 'Movie']
        tv_shows = sort_df['title'][sort_df['type'] == 'TV Show']
        
        similar_movies = []
        similar_tv_shows = []
        
        for i, movie in enumerate(movies):
            similar_movies.append('{}. {}'.format(i + 1, movie))
        
        for i, tv_show in enumerate(tv_shows):
            similar_tv_shows.append('{}. {}'.format(i + 1, tv_show))
        
        return similar_movies, similar_tv_shows

    def find_id(self, name):
        for index, string in enumerate(self.df['title']):
            if re.search(name, string):
                return index
        return -1

@app.route('/recommend', methods=['GET'])
def recommend():
    title = request.args.get('title')
    if not title:
        logging.warning("No title provided for recommendation")
        return jsonify({'error': 'Please provide a title for recommendation'}), 400

    # Initialize FlixHub
    flix_hub = FlixHub(netflix_data, cosine_sim)
    
    movies, tv_shows = flix_hub.recommendation(title, total_result=10, threshold=0.5)
    if not movies and not tv_shows:
        logging.warning(f"No recommendations found for title '{title}'")
        return jsonify({'error': f"No recommendations found for title '{title}'"}), 404

    logging.info(f"Recommendations generated successfully for title '{title}'")
    
    return jsonify({'movies': movies, 'tv_shows': tv_shows})

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
