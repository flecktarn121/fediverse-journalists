import csv
import spacy
import constants
import shifterator
import json
import os


class WordShiftGraphGenerator:

    def __init__(self):
        self.term_frequencies_corpus_a = {}
        self.term_frequencies_corpus_b = {}
        self.nlp = spacy.load(constants.SPACY_MODEL)
    
    def load_precalculated_frequencies(self, filename_corpus_a, filename_corpus_b):
        self.term_frequencies_corpus_a = self.__load_frequencies_from_file(filename_corpus_a)
        self.term_frequencies_corpus_b = self.__load_frequencies_from_file(filename_corpus_b)
    
    def __load_frequencies_from_file(filename):
        frequencies = {}
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                frequencies[row['term']] = int(row['frequency'])
    
        return frequencies
    
    def calculate_frequencies(self, corpus, frequencies):
        doc = self.nlp(corpus)
        for token in doc:
            if token.text not in frequencies:
                frequencies[token.text] = 0
            
            frequencies[token.text] += 1
    
    def save_frequencies(self, directory):
        self.__save_frequencies(directory + 'corpus_a.csv', self.term_frequencies_corpus_a)
        self.__save_frequencies(directory + 'corpus_b.csv', self.term_frequencies_corpus_b)
    
    def __save_frequencies(self, filename, frequencies):
        with open(filename, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['term', 'frequency'])
            writer.writeheader()
            for term, frequency in frequencies.items():
                writer.writerow({'term': term, 'frequency': frequency})

    def generate_graph(self, label_corpus_a, label_corpus_b, title): 
        jsd_shift = shifterator.JSDivergenceShift(type2freq_1=self.term_frequencies_corpus_a, type2freq_2=self.term_frequencies_corpus_b, weight_1=0.5, weight_2=0.5, base=2, alpha=1)
        jsd_shift.get_shift_graph(title=title, label_1=label_corpus_a, label_2=label_corpus_b, filename='word_shift_graphs/' + title + '.html')
    
    def load_corpus(self, directory):
        corpus = []
        for filename in os.listdir(directory):
            with open(directory + filename, 'r', encoding='utf-8') as file:
                posts = json.load(file)
                corpus += [post['text'] for post in posts]
        
        return ' '.join(corpus)

if __name__ == '__main__':
    generator = WordShiftGraphGenerator()
    corpus = generator.load_corpus(constants.NORMALIZED_DIRECTORY + 'twitter/')  
    generator.calculate_frequencies(corpus, generator.term_frequencies_corpus_a)
    corpus = generator.load_corpus(constants.NORMALIZED_DIRECTORY + 'mastodon/')
    generator.calculate_frequencies(corpus, generator.term_frequencies_corpus_b)

    generator.save_frequencies(constants.FREQUENCIES_DIRECTORY)

    generator.generate_graph('Twitter', 'Mastodon', 'Twitter vs. Mastodon')

