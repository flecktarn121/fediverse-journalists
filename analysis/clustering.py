import ijson
import os
import constants
import pickle
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


class Clusterer:

    def load_posts_from_directory(self, directory):
        posts_texts = []
        for filename in os.listdir(directory):
            with open(f'{directory}/{filename}', 'r', encoding='utf-8') as file:
                json_posts = ijson.items(file, 'item')
                posts_texts += [json_post['text'].lower() for json_post in json_posts]
        
        return posts_texts

    def vectorize_texts(self, texts):
        vectorizer = TfidfVectorizer(encoding='utf-8', lowercase=True, stop_words='english', max_features=10000, ngram_range=(1, 3))
        vectors = vectorizer.fit_transform(texts)
        return vectors
    
    def cluster_texts(self, vectors):
        
        kmeans = KMeans(n_clusters=constants.NUM_CLUSTERS, init='k-means++', max_iter=1000, n_init=1, verbose=True).fit(vectors)
        return kmeans

if __name__ == '__main__':
    clusterer = Clusterer()
    texts = clusterer.load_posts_from_directory(constants.NORMALIZED_DIRECTORY + '/mastodon/final')
    vectorized_texts = clusterer.vectorize_texts(texts)
    clusters = clusterer.cluster_texts(vectorized_texts)
    pickle.dump(clusters, open('mastodon.pkl', 'wb'))
    
    