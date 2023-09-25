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
    
    result = tw_aligned_embs[common_idx['trump']].dot(mast_aligned_embs[common_idx['trump']]) 
    print(f'Cosine similarity between trump in twitter and mastodon: {result}')

    return
    politics_words = [
                  'freedom', 'justice', 'equality', 'democracy', # political abstractions
                  'abortion', 'immigration', 'welfare', 'taxes', # partisan political issues   
                  'democrat', 'republican' # political parties               
                 ] # from Rodriguez and Spirling 2021
    for word in politics_words:
        print(f'Querying twitter model for {word}')
        near_words = models.query_models(word, twitter_model)
        for word in near_words:
            print(word)

        print(f'Querying mastodon model for {word}')
        near_words = models.query_models(word, mastodon_model)
        for word in near_words:
            print(word)

if __name__ == '__main__':
    main()