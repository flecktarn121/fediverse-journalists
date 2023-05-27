import constants
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
        self.term_frequencies = {}
        self.term_frequencies_by_timestamp = {}
    
    def load_posts_from_directory(self, directory):
        posts = []
        for filename in os.listdir(directory):
            with open(f'{directory}/{filename}', 'r', encoding='utf-8') as file:
                json_posts = ijson.items(file, 'item')
                posts += [Post.load_from_json(json_post) for json_post in json_posts]
                self.__tokenize_posts(posts)
                for post in posts:
                    self.update_frequencies(post)
                    self.update_frequencies_by_time(post,constants.ROUNDING_TIME)
            break
    
    def update_frequencies(self, post):
        for token in post.tokenized_text:
            if token not in self.term_frequencies:
                self.term_frequencies[token] = 0
            self.term_frequencies[token] += 1
    
    def update_frequencies_by_time(self, post, rounding_time):
        post.timestamp = self.__round_timestamp(post.timestamp, rounding_time)

        if post.timestamp not in self.term_frequencies_by_timestamp:
            self.term_frequencies_by_timestamp[post.timestamp] = {}
        
        tokens = chain.from_iterable(post.tokenized_text) 
        token_frequencies = Counter(tokens)

        for token, frequency in token_frequencies.items():
            if token not in self.term_frequencies_by_timestamp[post.timestamp]:
                self.term_frequencies_by_timestamp[post.timestamp][token] = 0
            self.term_frequencies_by_timestamp[post.timestamp][token] += frequency
    
    def save_frequencies(self, filename):
        self.__save_frequencies(self.term_frequencies, filename)
    
    def save_frequencies_by_time(self, filename):
        self.__save_frequencies(self.term_frequencies_by_timestamp, filename)

    def load_precalculated_frequencies_from_file(filename):
        frequencies = {}
        with open(filename, 'r', encoding='utf-8') as file:
            frequencies = json.load(file)
    
        return frequencies

    def __save_frequencies(self, frequencies, filename):
        with open(f'{constants.FREQUENCIES_DIRECTORY}/{filename}', 'w', encoding='utf-8') as file:
            json.dump(frequencies, file, indent=4, ensure_ascii=False)
        
    def __round_timestamp(self, timestamp, rounding):
        discard = datetime.timedelta(minutes=timestamp.minute % rounding,
                               seconds=timestamp.second,
                               microseconds=timestamp.microsecond)
        timestamp -= discard
  
        if discard >= datetime.timedelta(minutes=rounding/2):
            timestamp += datetime.timedelta(minutes=rounding)
        
        return timestamp

    def __tokenize_posts(self, posts):
        for post in posts:
            tokens = post.text.split(' ') #already processed, no need to use tokenizer
            post.tokenized_text = [token.lower() for token in tokens if token in self.common_words or len(self.common_words) == 0]

    def load_common_words(self):
        with open(constants.COMMON_WORDS, 'r', encoding='utf-8') as file:
            for line in file:
                self.common_words.add(line.strip('\t')[0])
    

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    frequencies_calculator = FrequenciesCalculator()
    frequencies_calculator.load_posts_from_directory(constants.NORMALIZED_DIRECTORY+'/mastodon')
    frequencies_calculator.save_frequencies_by_time('frequencies_by_time.json')
    frequencies_calculator.save_frequencies('frequencies.json')