import constants
import shifterator
from frequencies import FrequenciesCalculator


class WordShiftGraphGenerator:

    def __init__(self):
        self.term_frequencies_corpus_a = {}
        self.term_frequencies_corpus_b = {}
    
    def generate_graph(self, label_corpus_a, label_corpus_b, title): 
        jsd_shift = shifterator.EntropyShift(type2freq_1=self.term_frequencies_corpus_a, type2freq_2=self.term_frequencies_corpus_b, base=2, alpha=1)
        #jsd_shift.get_shift_graph(title=title, label_1=label_corpus_a, label_2=label_corpus_b, filename= title + '.svg')
        #same line but without showing the graph
        jsd_shift.get_shift_graph(title=title, label_1=label_corpus_a, label_2=label_corpus_b, filename= title + '.svg', show_plot=False)
    
if __name__ == '__main__':
    frequenciesCalculator = FrequenciesCalculator()

    
    twitter_frequencies = frequenciesCalculator.load_precalculated_frequencies_from_file(constants.FREQUENCIES_DIRECTORY + '/twitter.json')


    
    mastodon_frequencies = frequenciesCalculator.load_precalculated_frequencies_from_file(constants.FREQUENCIES_DIRECTORY + '/mastodon.json')

    generator = WordShiftGraphGenerator()
    generator.term_frequencies_corpus_a = twitter_frequencies
    generator.term_frequencies_corpus_b = mastodon_frequencies

    generator.generate_graph('Twitter', 'Mastodon', 'Twitter vs. Mastodon')

