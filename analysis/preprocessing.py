import spacy
import logging
import emoji
import validators
import json
import constants
from nel import NamedEntityLinker
from spacy_langdetect import LanguageDetector
from spacy.language import Language


class PreProcessor:

    def __init__(self):
        self.file_counter = 0
        self.linker = NamedEntityLinker()
        self.nlp = spacy.load(constants.SPACY_MODEL)
        self.posts_source = ''

    def preprocess_posts(self, posts):

        logging.info('Tokenizando posts...')
        tokenized_posts = self.__tokenize(posts)
        logging.info('Limpiando posts...')
        tokenized_posts = self.__clean_posts(tokenized_posts)
        logging.info('Quitando emojis de los posts...')
        tokenized_posts = self.__remove_emoji(tokenized_posts)
        logging.info('Enlazando entidades de los posts...')
        self.linker.link([''.join(post.text).lower() for post in tokenized_posts])

        self.__save_posts_to_file(tokenized_posts, f'{constants.PREPROCESSED_DIRECTORY}/{self.posts_source}/preprocessed_')
    
    def normalize_posts(self, posts):
        logging.info('Normalizing posts...')
        posts = self.__remove_non_english_posts(posts)
        self.__substitute_entities_by_ids(posts)

        tokenized_posts = self.__tokenize(posts)
        self.__lematize_posts(tokenized_posts)

        logging.info('Saving normalized posts...')
        self.__save_posts_to_file(tokenized_posts, f'{constants.NORMALIZED_DIRECTORY}/{self.posts_source}/normalized_')
    
    def __remove_non_english_posts(self, posts):
        if not self.nlp.has_pipe("language_detector"):
            Language.factory("language_detector", func=self.create_lang_detector)
            self.nlp.add_pipe('language_detector', last=True)

        posts = [post for post in posts if self.__is_post_in_english(post)]
        return posts
    
    def create_lang_detector(self, nlp, name):
        return LanguageDetector()

    def __is_post_in_english(self, post):
        doc = self.nlp(post.text)
        return doc._.language['language'] == 'en'

    def __substitute_entities_by_ids(self, posts):
        for post in posts:
            post.text = self.linker.substitute_entites_by_ids(post.text)

    def __tokenize(self, posts):
        nlp = spacy.load(constants.SPACY_MODEL)
        for post in posts:
            post.tokenized_text += ([token for token in nlp(post.text)])

        return posts

    def __remove_emoji(self, tokenized_posts):
        for post in tokenized_posts:
            new_post_text = []
            for token in post.tokenized_text:
                text = token.text
                if emoji.is_emoji(text):
                    text = emoji.demojize(text, delimiters=('', '')).replace('_', ' ')
                new_post_text.append(text)
            post.text = ' '.join(new_post_text)
        
        return tokenized_posts

    def __clean_posts(self, tokenized_posts):
        for post in tokenized_posts:
            post.tokenized_text = [token for token in post.tokenized_text if self.__is_valid_token(token)]

        return tokenized_posts

    def __lematize_posts(self, tokenized_posts):
        lemmatized_text = []
        for post in tokenized_posts:
            lemmatized_text += [token.lemma_ for token in post.tokenized_text if self.__is_word(token)]
            post.text = ' '.join(lemmatized_text)
            lemmatized_text = []

        return tokenized_posts

    def __save_posts_to_file(self, preprocessed_posts, base_filename):
        filename = f'{base_filename}{self.file_counter}.json'
        with open(filename, 'w') as f:
            json.dump([post.to_dict() for post in preprocessed_posts], f, indent=4, default=str)

        self.file_counter += 1

    def __is_word(self, token):
        is_word = True
        
        is_word &= not token.is_stop
        is_word &= not token.is_punct
        is_word &= not token.is_space

        return is_word

    def __is_valid_token(self, token):
        is_valid = True

        is_valid &= not validators.url(token.text)
        is_valid &= not self.__is_username(token.text)
        is_valid &= not self.__is_hashtag(token.text)

        return is_valid

    def __is_username(self, text):
        return text.startswith('@')

    def __is_hashtag(self, text):
        return text.startswith('#')