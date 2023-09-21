from typing import Any
import numpy as np
from copy import deepcopy
from gensim.models import Word2Vec #type: ignore
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import constants #type ignore
import corpus


def get_word2vec_model(corpus: str) -> Word2Vec:
    return Word2Vec(corpus, window=10, min_count=10, seed=42, workers=1)

def near_neighbors(embeddings, query, word2rownum, rownum2word, k=5) -> list: 
    sims = np.dot(embeddings, embeddings[word2rownum[query]])
    indices = np.argsort(sims)
    return [(rownum2word[index], sims[index]) for index in indices[1:k+1]]

def w2v_to_numpy(model: Word2Vec) -> Any:
    model.wv.init_sims()
    embeddings = deepcopy(model.wv.get_normed_vectors())
    idx = {w:i for i, w in enumerate (model.wv.index_to_key)}
    iidx = {i:w for i, w in enumerate (model.wv.index_to_key)}
    return embeddings, (idx, iidx)

def query_models(query: str, model: Word2Vec) -> list:
    embs, (idx, iidx) = w2v_to_numpy(model)
    return near_neighbors(embs, query, idx, iidx, k=10)

def main() -> None:
    print('Loading twitter corpus')
    twitter_corpus = corpus.get_corpus_from_file(constants.CORPUS_DIRECTORY+ '/twitter_corpus.txt')
    print('Loading mastodon corpus')
    mastodon_corpus = corpus.get_corpus_from_file(constants.CORPUS_DIRECTORY+ '/mastodon_corpus.txt')
    print('Creating twitter model')
    #twitter_model = get_word2vec_model(twitter_corpus)
    #print('Saving twitter model')
    #twitter_model.save(constants.CORPUS_DIRECTORY+ '/twitter_model')
    twitter_model = Word2Vec.load(constants.CORPUS_DIRECTORY+ '/twitter_model')
    print('Creating mastodon model')
    #mastodon_model = get_word2vec_model(mastodon_corpus)
    #print('Saving mastodon model')
    #mastodon_model.save(constants.CORPUS_DIRECTORY+ '/mastodon_model')
    mastodon_model = Word2Vec.load(constants.CORPUS_DIRECTORY+ '/mastodon_model')

    print('Querying twitter model for trump')
    near_words = query_models('trump', twitter_model)
    for word in near_words:
        print(word)


    print('Querying mastodon model for trump')
    near_words = query_models('trump', mastodon_model)
    for word in near_words:
        print(word)

if __name__ == '__main__':
    main()
