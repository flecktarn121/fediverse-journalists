import constants
import shifterator
from frequencies import FrequenciesCalculator


class WordShiftGraphGenerator:

    def __init__(self):
        self.term_frequencies_corpus_a = {}
        self.term_frequencies_corpus_b = {}
    
    def generate_graph(self, label_corpus_a, label_corpus_b, title): 
        jsd_shift = shifterator.JSDivergenceShift(type2freq_1=self.term_frequencies_corpus_a, type2freq_2=self.term_frequencies_corpus_b, weight_1=0.5, weight_2=0.5, base=2, alpha=1)
        jsd_shift.get_shift_graph(title=title, label_1=label_corpus_a, label_2=label_corpus_b, filename='word_shift_graphs/' + title + '.html')
    
if __name__ == '__main__':
    frequenciesCalculator = FrequenciesCalculator()

    frequenciesCalculator.load_posts_from_directory(constants.NORMALIZED_DIRECTORY + 'twitter/')
    frequenciesCalculator.update_frequencies()
    frequenciesCalculator.save_frequencies(constants.FREQUENCIES_DIRECTORY + 'twitter.json')
    twitter_frequencies = frequenciesCalculator.term_frequencies

    frequenciesCalculator.load_posts_from_directory(constants.NORMALIZED_DIRECTORY + 'mastodon/')
    frequenciesCalculator.update_frequencies()
    frequenciesCalculator.save_frequencies(constants.FREQUENCIES_DIRECTORY + 'mastodon.json')
    mastodon_frequencies = frequenciesCalculator.term_frequencies

    generator = WordShiftGraphGenerator()
    generator.term_frequencies_corpus_a = twitter_frequencies
    generator.term_frequencies_corpus_b = mastodon_frequencies

    generator.generate_graph('Twitter', 'Mastodon', 'Twitter vs. Mastodon')

