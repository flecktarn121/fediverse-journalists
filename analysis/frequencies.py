import constants
import spacy
import datetime
import logging
import os
import ijson
import json
from post import Post
from collections import Counter
from itertools import chain


class FrequenciesCalculator:

    def __init__(self):
        self.common_words = set()
        self.nlp = spacy.load(constants.SPACY_MODEL)
        self.term_frequencies = {}
        self.term_frequencies_by_timestamp = {}
    
    def load_posts_from_directory(self, directory):
        posts = []
        for filename in os.listdir(directory):
            with open(f'{directory}/{filename}', 'r', encoding='utf-8') as file:
                posts = ijson.items(file, 'item')
                posts = [Post.load_from_json(post) for post in posts]
                self.__tokenize_posts(posts)
                for post in posts:
                    #self.update_frequencies(post)
                    self.update_frequencies_by_time(post,constants.ROUNDING_TIME)
    
    def update_frequencies(self, post):
        for token in post.tokenized_text + post.entities:
            if token not in self.term_frequencies:
                self.term_frequencies[token] = 0
            self.term_frequencies[token] += 1
    
    def update_frequencies_by_time(self, post, rounding_time):
        post.timestamp = self.__round_timestamp(post.timestamp, rounding_time)

        if post.timestamp not in self.term_frequencies_by_timestamp:
            self.term_frequencies_by_timestamp[post.timestamp.timestamp()] = {}
        
        token_frequencies = Counter(post.tokenized_text)

        for token, frequency in token_frequencies.items():
            if token not in self.term_frequencies_by_timestamp[post.timestamp.timestamp()]:
                self.term_frequencies_by_timestamp[post.timestamp.timestamp()][token] = 0
            self.term_frequencies_by_timestamp[post.timestamp.timestamp()][token] += frequency
    
    def save_frequencies(self, filename):
        self.__save_frequencies(self.term_frequencies, filename)
    
    def save_frequencies_by_time(self, filename):
        self.__save_frequencies(self.term_frequencies_by_timestamp, filename)

    def load_precalculated_frequencies_from_file(self, filename):
        frequencies = {}
        with open(filename, 'r', encoding='utf-8') as file:
            frequencies = dict(sorted(json.load(file).items()))
    
        return frequencies

    def __save_frequencies(self, frequencies, filename):
        with open(f'{constants.FREQUENCIES_DIRECTORY}/{filename}', 'w', encoding='utf-8') as file:
            json.dump(frequencies, file, indent=4, ensure_ascii=False)
        
    def __round_timestamp(self, timestamp, rounding):
        #new_timestamp = timestamp - datetime.timedelta(days=timestamp.weekday())
        new_timestamp = timestamp.replace(hour=0, minute=0, second=0, microsecond=0)
        return new_timestamp

    def __tokenize_posts(self, posts):
        for post in posts:
            tokens = post.text.split(' ') #already processed, no need to use tokenizer
            tokens = [token for token in tokens if 'http'not in token and 'tag' not in token and '@' not in token]
            post.tokenized_text = [token.lower() for token in tokens if token in self.common_words or len(self.common_words) == 0]

if __name__ == '__main__':
    frequenciesCalculator = FrequenciesCalculator()
    
    frequenciesCalculator.load_posts_from_directory(constants.NORMALIZED_DIRECTORY + '/twitter/')
    #frequenciesCalculator.save_frequencies('/twitter_nouns.json')
    frequenciesCalculator.save_frequencies_by_time('/twitter_by_time.json')
    twitter_frequencies = frequenciesCalculator.term_frequencies

    frequenciesCalculator.load_posts_from_directory(constants.NORMALIZED_DIRECTORY + '/mastodon/final/')
    #frequenciesCalculator.save_frequencies('/mastodon_nouns.json')
    frequenciesCalculator.save_frequencies_by_time('/mastodon_by_time.json')
    twitter_frequencies = frequenciesCalculator.term_frequencies