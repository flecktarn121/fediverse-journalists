import constants
import csv
import logging
from wordShiftGraphs import WordShiftGraphGenerator
from frequencies import FrequenciesCalculator
from matplotlib import pyplot as plt
from datetime import datetime

class GraphGenerator:

    def __init__(self):
        self.common_words = self.__load_common_words()
        self.hedometer_lexicon = self.__load_hedometer_lexicon()
        self.frequencies_by_interval_a = {}
        self.frequencies_by_interval_b = {}
    
    def __load_hedometer_lexicon(self):
        lexicon = {}
        with open(constants.HEDOMETER_LEXICON, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, dialect='excel')    
            for row in reader:
                lexicon[row['Word']] = float(row['Happiness Score'])
    
        return lexicon

    def __load_common_words(self):
        common_words = set()
        with open(constants.COMMON_WORDS, 'r', encoding='utf-8') as file:
            for line in file:
                common_words.add(line.strip('\t')[0])
        
        return common_words
    
   
    def calculate_happiness(self, frequencies_by_interval):
        logging.info('Calculating happiness...')
        happiness_by_timestamp = {}
        for timestamp, interval_tokens in frequencies_by_interval.items():
            if len(interval_tokens) == 0:
                happiness_by_timestamp[timestamp] = 0
            else:
                happiness_by_timestamp[timestamp] = self.__meassure_interval_hapiness(interval_tokens)

        return happiness_by_timestamp 
    
    def plot(self, happiness_by_timestamp_a, happiness_by_timestamp_b, show=False):
        #crea las keys en formato legible (día/mes/año)
        keys_a = [datetime.fromtimestamp(float(timestamp)).strftime('%d/%m/%Y') for timestamp in happiness_by_timestamp_a.keys()]
        keys_b = [datetime.fromtimestamp(float(timestamp)).strftime('%d/%m/%Y') for timestamp in happiness_by_timestamp_b.keys()]
        logging.info('Plotting...')
        plt.plot(keys_a, happiness_by_timestamp_a.values(), label='Twitter')
        plt.plot(keys_b, happiness_by_timestamp_b.values(), label='Mastodon')
        plt.xlabel('Time')
        plt.xticks(rotation=45)
        plt.ylabel('Happiness')
        plt.legend()
        plt.savefig('happiness.svg') 
        if show: 
            plt.show()

    def __meassure_interval_hapiness(self, interval_tokens):
        number_of_tokens = sum(interval_tokens.values())

        #dictionary of tokens with their happiness score multiplied by their frequency
        happy_tokens = {token: frequency * self.hedometer_lexicon[token] for token, frequency in interval_tokens.items() if token in self.hedometer_lexicon}

        interval_happiness = sum(happy_tokens.values())

        return interval_happiness / number_of_tokens
    
    def print_words_shift_graphs(self, frequencies_a_by_timestamp, happiness_a_by_timestamp, frequencies_b_by_timestamp, happiness_b_by_timestamp):
        logging.info('Printing word shift graphs...')
        timestamps = set(frequencies_a_by_timestamp.keys()).union(set(frequencies_b_by_timestamp.keys()))
        for timestamp in timestamps:
            if happiness_a_by_timestamp[timestamp] > 0 or happiness_b_by_timestamp[timestamp] > 0:
                self.__print_word_shift_graph(frequencies_a_by_timestamp[timestamp], frequencies_b_by_timestamp[timestamp], timestamp)
    
    def __print_word_shift_graph(self, frequencies_a, frequencies_b, timestamp):
        wordShiftGraphGenerator = WordShiftGraphGenerator()
        wordShiftGraphGenerator.term_frequencies_corpus_a = frequencies_a
        wordShiftGraphGenerator.term_frequencies_corpus_b = frequencies_b
        wordShiftGraphGenerator.generate_graph('Twitter', 'Mastodon', f'Twitter_vs_Mastodon_{datetime.fromtimestamp(float(timestamp)).strftime("%Y-%m-%d")}')

    

if __name__ == '__main__':
    graphGenerator = GraphGenerator()
    frequencies_calculator = FrequenciesCalculator()
    frequencies_twitter = frequencies_calculator.load_precalculated_frequencies_from_file(constants.FREQUENCIES_DIRECTORY + '/twitter_by_time.json')
    happiness_twitter = graphGenerator.calculate_happiness(frequencies_twitter)
    frequencies_mastodon = frequencies_calculator.load_precalculated_frequencies_from_file(constants.FREQUENCIES_DIRECTORY + '/mastodon_by_time.json')
    happiness_mastodon = graphGenerator.calculate_happiness(frequencies_mastodon)
    graphGenerator.print_words_shift_graphs(frequencies_twitter, happiness_twitter, frequencies_mastodon, happiness_mastodon)
    graphGenerator.plot(happiness_twitter, happiness_mastodon, True)

