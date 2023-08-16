import numpy as np
from gensim.models import Word2Vec


def get_word2vec_model(corpus: str) -> Word2Vec:
    return Word2Vec(corpus, window=10, min_count=10, seed=42, workers=1)

def near_neighbors(embeddings, query, word2rownum, rownum2word, k=5) -> list: 
    sims = np.dot(embeddings, embeddings[word2rownum[query]])
    indices = np.argsort(sims)
    return [(rownum2word[index], sims[index]) for index in indices[1:k+1]]

def query_models(query: str, model: Word2Vec) -> list:
    #for item in near_neighbors(model, query, )
    pass