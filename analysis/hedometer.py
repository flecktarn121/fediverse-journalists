import constants
import csv
import logging
from matplotlib import pyplot as plt

class GraphGenerator:

    def __init__(self):
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
   
    def calculate_happiness(self, frequencies_by_interval):
        logging.info('Calculating happiness...')
        happiness_by_timestamp = {}
        for timestamp, interval_tokens in frequencies_by_interval.items():
            happiness_by_timestamp[timestamp] = self.__meassure_interval_hapiness(interval_tokens)

        return happiness_by_timestamp 
    
    def plot(self, happiness_by_timestamp_a, happiness_by_timestamp_b):
        logging.info('Plotting...')
        #plot both happinesses in the same graph, but with different scales
        fig, ax1 = plt.subplots()
        ax1.plot(happiness_by_timestamp_a.keys(), happiness_by_timestamp_a.values(), 'b-')
        ax1.set_xlabel('time (s)')
        ax1.set_ylabel('happiness', color='b')
        ax1.tick_params('y', colors='b')

        ax2 = ax1.twinx()
        ax2.plot(happiness_by_timestamp_b.keys(), happiness_by_timestamp_b.values(), 'r-')
        ax2.set_ylabel('happiness', color='r')
        ax2.tick_params('y', colors='r')

        fig.tight_layout()
        plt.show()

    def __meassure_interval_hapiness(self, interval_tokens):
        number_of_tokens = sum(interval_tokens.values())

        #dictionary of tokens with their happiness score multiplied by their frequency
        happy_tokens = {token: frequency * self.hedometer_lexicon[token] for token, frequency in interval_tokens.items() if token in self.hedometer_lexicon}

        interval_happiness = sum(happy_tokens.values())

        return interval_happiness / number_of_tokens

if __name__ == '__main__':
    graphGenerator = GraphGenerator()
    graphGenerator.load_posts()
    print(graphGenerator.posts_by_timestamp)