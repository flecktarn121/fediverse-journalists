from typing import Any
import numpy as np
from copy import deepcopy
from gensim.models import Word2Vec #type: ignore
from gensim.models.word2vec import LineSentence #type: ignore
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import constants #type ignore
import json
import corpus as cp


def get_word2vec_model(corpus_filename: str) -> Word2Vec:
    corpus = LineSentence(corpus_filename)
    return Word2Vec(corpus, seed=42, workers=4)

def near_neighbors(embeddings, query, word2rownum, rownum2word, k=5) -> list: 
    # save word2rownum to a file

    if query not in word2rownum:
        print(f'{query} not in vocabulary.')
        return []
    sims = np.dot(embeddings, embeddings[word2rownum[query]])
    indices = np.argsort(sims)
    return [(rownum2word[index], sims[index]) for index in indices[1:k+1]]

def w2v_to_numpy(model: Word2Vec) -> Any:
    model.wv.fill_norms()


    embeddings = deepcopy(model.wv.get_normed_vectors())
    idx = {w:i for i, w in enumerate (model.wv.index_to_key)}
    with open('wv.json', 'w') as f:
        json.dump(idx, f)
    iidx = {i:w for i, w in enumerate (model.wv.index_to_key)}
    return embeddings, (idx, iidx)

def query_models(query: str, model: Word2Vec) -> list:
    embs, (idx, iidx) = w2v_to_numpy(model)
    return near_neighbors(embs, query, idx, iidx, k=10)

def main() -> None:
    print('Creating twitter model')
    corpus = cp.get_corpus_from_file(constants.CORPUS_DIRECTORY + '/twitter_corpus.txt')
    #twitter_model = get_word2vec_model(corpus)
    #twitter_model.save(constants.CORPUS_DIRECTORY+ '/twitter_model')

    print('Creating mastodon model')
    twitter_model = Word2Vec.load(constants.CORPUS_DIRECTORY+ '/twitter_model')
    corpus = cp.get_corpus_from_file(constants.CORPUS_DIRECTORY + '/mastodon_corpus.txt')
    #mastodon_model = get_word2vec_model(corpus)
    #mastodon_model.save(constants.CORPUS_DIRECTORY+ '/mastodon_model')

    print('Creating mastodon model')
    mastodon_model = Word2Vec.load(constants.CORPUS_DIRECTORY+ '/mastodon_model')

    politics_words = [
                  'freedom', 'justice', 'equality', 'democracy', # political abstractions
                  'abortion', 'immigration', 'welfare', 'taxes', # partisan political issues   
                  'democrat', 'republican' # political parties               
                 ] # from Rodriguez and Spirling 2021
    for word in politics_words:
        print(f'Querying twitter model for {word}')
        near_words = query_models(word, twitter_model)
        for word in near_words:
            print(word)

        print(f'Querying mastodon model for {word}')
        near_words = query_models(word, mastodon_model)
        for word in near_words:
            print(word)

if __name__ == '__main__':
    main()
