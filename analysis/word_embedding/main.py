import models
import aligment
import corpus as cp
from gensim.models import Word2Vec #type: ignore
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import constants #type ignore


def main() -> None:
    print('Creating twitter model')
    #twitter_model = models.get_word2vec_model(constants.CORPUS_DIRECTORY + '/twitter_corpus.txt')
    #twitter_model.save(constants.CORPUS_DIRECTORY+ '/twitter_model')
    twitter_model = Word2Vec.load(constants.CORPUS_DIRECTORY+ '/twitter_model')

    print('Creating mastodon model')
    #mastodon_model = models.get_word2vec_model(constants.CORPUS_DIRECTORY + '/mastodon_corpus.txt')
    #mastodon_model.save(constants.CORPUS_DIRECTORY+ '/mastodon_model')
    mastodon_model = Word2Vec.load(constants.CORPUS_DIRECTORY+ '/mastodon_model')

    print('Aligning models')
    tw_aligned_embs, mast_aligned_embs, (common_idx, common_iidx) = aligment.align_models(twitter_model, mastodon_model)
    
    politics_words = [
                  'freedom', 'justice', 'equality', 'democracy', # political abstractions
                  'abortion', 'immigration', 'welfare', 'taxes', # partisan political issues   
                  'democrat', 'republican' # political parties               
                 ] # from Rodriguez and Spirling 2021
    for word in politics_words:
        print(f'Cosine similarity for {word}')
        if word not in common_idx:
            print(f'{word} not found in both corpora')
            continue
        result = tw_aligned_embs[common_idx[word]].dot(mast_aligned_embs[common_idx[word]]) 
        print(f'Cosine similarity between {word} in twitter and mastodon: {result}')
        

if __name__ == '__main__':
    main()