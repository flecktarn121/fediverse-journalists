import spacy
import logging
import emoji
import validators
import json
import constants
from nel import NamedEntityLinker
from spacy_langdetect import LanguageDetector


class PreProcessor:

    def __init__(self):
        self.file_counter = 0
        self.linker = NamedEntityLinker()
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

        self.__save_posts_to_file(tokenized_posts)
    
    def normalize_posts(self, posts):
        self.__remove_non_english_posts(posts)
        self.__substitute_entities_by_ids(posts)
        self.__lematize_posts(posts)
        self.__save_posts_to_file(posts)
    
    def __remove_non_english_posts(self, posts):
        posts = [post for post in posts if self.__is_post_in_english(post)]
        return posts

    def __is_post_in_english(self, post):
        nlp = spacy.load(constants.SPACY_MODEL)
        nlp.add_pipe(LanguageDetector(), name='language_detector', last=True)
        doc = nlp(post.text)
        return doc._.language['language'] == 'en'

    def __substitute_entities_by_ids(self, posts):
        self.linker.load_entities_from_file("data/entities/entities.json")
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
        for post in tokenized_posts:
            post = [token.lemma_ for token in post]

        return tokenized_posts

    def __save_posts_to_file(self, preprocessed_posts):
        filename = f'{constants.PREPROCESSED_DIRECTORY}/{self.posts_source}/preprocessed_{self.file_counter}.json'
        with open(filename, 'w') as f:
            json.dump([post.to_dict() for post in preprocessed_posts], f, indent=4, default=str)

        self.file_counter += 1


    def __is_valid_token(self, token):
        is_valid = True

        #is_valid &= not token.is_stop
        #is_valid &= not token.is_punct
        #is_valid &= not token.is_space
        is_valid &= not validators.url(token.text)
        is_valid &= not self.__is_username(token.text)
        is_valid &= not self.__is_hashtag(token.text)

        return is_valid

    def __is_username(self, text):
        return text.startswith('@')

    def __is_hashtag(self, text):
        return text.startswith('#')