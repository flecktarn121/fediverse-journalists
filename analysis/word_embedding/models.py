from typing import Any
import numpy as np
from copy import deepcopy
from gensim.models import Word2Vec #type: ignore
from gensim.models.word2vec import LineSentence #type: ignore
import os, sys
import json
import corpus as cp


def get_word2vec_model(corpus_filename: str) -> Word2Vec:
    corpus = LineSentence(corpus_filename)
    return Word2Vec(corpus, seed=42, workers=4)

def near_neighbors(embeddings, query, word2rownum, rownum2word, k=5) -> list: 
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
    iidx = {i:w for i, w in enumerate (model.wv.index_to_key)}

    return embeddings, (idx, iidx)

def query_models(query: str, model: Word2Vec) -> list:
    embs, (idx, iidx) = w2v_to_numpy(model)
    return near_neighbors(embs, query, idx, iidx, k=10)