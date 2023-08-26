import corpus
import numpy as np
from copy import deepcopy
from gensim.models import Word2Vec #type: ignore
import sys
sys.path.append('..')
import constants


def get_word2vec_model(corpus: str) -> Word2Vec:
    return Word2Vec(corpus, window=10, min_count=10, seed=42, workers=1)

def near_neighbors(embeddings, query, word2rownum, rownum2word, k=5) -> list: 
    sims = np.dot(embeddings, embeddings[word2rownum[query]])
    indices = np.argsort(sims)
    return [(rownum2word[index], sims[index]) for index in indices[1:k+1]]

def w2v_to_numpy(model: Word2Vec) -> np.array:
    model.wv.init_sims()
    embeddings = deepcopy(model.wv.vectors_norm)
    idx = {w:i for i, w in enumerate (model.wv.index2word)}
    iidx = {i:w for i, w in enumerate (model.wv.index2word)}
    return embeddings, (idx, iidx)

def query_models(query: str, model: Word2Vec) -> list:
    embs, (idx, iidx) = w2v_to_numpy(model)
    for item in near_neighbors(embs, query, idx, iidx, k=10):
        print(item)

def main() -> None:
    twitter_corpus = corpus.get_corpus_from_directory(constants.NORMALIZED_DIRECTORY + '/twitter')
    mastodon_corpus = corpus.get_corpus_from_directory(constants.NORMALIZED_DIRECTORY + '/mastodon')
    twitter_model = get_word2vec_model(twitter_corpus)
    mastodon_model = get_word2vec_model(mastodon_corpus)
    print('Querying twitter model')
    query_models('trump', twitter_model)

    print('Querying mastodon model')
    query_models('trump', mastodon_model)
