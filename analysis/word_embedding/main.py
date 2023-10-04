import models
import csv
import aligment
import corpus as cp
import numpy as np
from gensim.models import Word2Vec #type: ignore
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import constants #type ignore


def get_different_words(model1: Word2Vec, model2: Word2Vec, lexicon: set[str]) -> None:
    #get the words from the lexicon that are exclusevely in each of the models
    model1_words = set(model1.wv.vocab.keys()).intersection(lexicon)
    model2_words = set(model2.wv.vocab.keys()).intersection(lexicon)
    model1_exclusive_words = model1_words.difference(model2_words)
    model2_exclusive_words = model2_words.difference(model1_words)

    return model1_exclusive_words, model2_exclusive_words

def get_model(model_name: str) -> Word2Vec:
    #model = models.get_word2vec_model(constants.CORPUS_DIRECTORY + '/twitter_corpus.txt')
    #model.save(constants.CORPUS_DIRECTORY+ '/twitter_model')
    model = Word2Vec.load(constants.CORPUS_DIRECTORY+ f'/{model_name}_model')
    return model

def main() -> None:
    print(f'Creating twitter model')
    twitter_model = get_model('twitter')

    print('Creating mastodon model')
    mastodon_model = get_model('mastodon')

    with open(constants.RESOURCES_DIRECTORY + 'profanities.csv', 'r', encoding='utf-8') as f:
        profanities = {row[0] for row in csv.reader(f)}

    calculate_different_words(twitter_model, mastodon_model, profanities)

    print('Aligning models')
    tw_aligned_embs, mast_aligned_embs, (common_idx, common_iidx) = aligment.align_models(twitter_model, mastodon_model)
    
    cos_similarity_among_words(profanities, tw_aligned_embs, mast_aligned_embs, common_idx)

    near_neighbours_similarity(tw_aligned_embs, mast_aligned_embs, common_idx, common_iidx)

def cos_similarity_among_words(lexicon, tw_aligned_embs, mast_aligned_embs, common_idx):
    cosine_similarity = {}
    for word in lexicon:
        if word not in common_idx:
            print(f'{word} not found in both corpora')
            continue
        result = tw_aligned_embs[common_idx[word]].dot(mast_aligned_embs[common_idx[word]]) 
        cosine_similarity[word] = result
        print(f'Cosine similarity between {word} in twitter and mastodon: {result}')
    
    with open(constants.RESULTS_DIRECTORY + '/cosine_similarity.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=['word', 'similarity'])
        writer.writeheader()
        for word, similarity in cosine_similarity.items():
            writer.writerow({'word': word, 'similarity': similarity})

def calculate_different_words(twitter_model: Word2Vec, mastodon_model: Word2Vec, lexicon: set[str]) -> None:

    tw_exclusive_words, mast_exclusive_words  = get_different_words(twitter_model, mastodon_model, lexicon)

    with open(constants.RESULTS_DIRECTORY + '/twitter_exclusive_words.csv', 'w') as f:
        writer = csv.writer(f)
        for word in tw_exclusive_words:
            writer.writerow([word])
    
    with open(constants.RESULTS_DIRECTORY + '/mastodon_exclusive_words.csv', 'w') as f:
        writer = csv.writer(f)
        for word in mast_exclusive_words:
            writer.writerow([word])

def near_neighbours_similarity(tw_aligned_embs, mast_aligned_embs, common_idx, common_iidx):
    similarities = {}
    with open(constants.RESOURCES_DIRECTORY + 'polemic_lexicon.csv', 'r', encoding='utf-8') as f:
        polemic_lexicon = {row[0] for row in csv.reader(f)}
    
    for word in polemic_lexicon:
        similarity = near_neighbours_sim_for_word(tw_aligned_embs, mast_aligned_embs, word, (common_idx, common_iidx), 10)
        similarities[word] = similarity
    
    with open(constants.RESULTS_DIRECTORY + '/near_neighbours_similarity.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=['word', 'similarity'])
        writer.writeheader()
        for word, similarity in similarities.items():
            writer.writerow({'word': word, 'similarity': similarity})

def near_neighbours_sim_for_word(embs1, embs2, word, indexes, k):
    idx, iidx = indexes
    nn1 = models.near_neighbors (embs1, word, idx, iidx, k=k)
    nn2 = models.near_neighbors (embs2, word, idx, iidx, k=k)

    common = {w for w, _ in nn1} | {w for w,_ in nn2}
    scores1 = np.array([embs1[idx[w]].dot (embs1[idx[word]]) for w in common])
    scores2 = np.array([embs2[idx[w]].dot (embs2[idx[word]]) for w in common])

    return np.dot (scores1, scores2)/(np.linalg.norm (scores1) * np.linalg.norm (scores2))

if __name__ == '__main__':
    main()