import spacy
import logging
import json
import csv
import constants
import re
from dateutil.parser import parse
from post import Post
from normalizing.nel import NamedEntityLinker
from spacy.tokens import Token
from spacy_langdetect import LanguageDetector # type: ignore
from spacy.language import Language


class PreProcessor:

    def __init__(self) -> None:
        self.file_counter = 0
        self.posts_source = ''

        self.linker = NamedEntityLinker()
        self.nlp = spacy.load(constants.SPACY_MODEL)

        self.misspellings = self.__load_misspellings()
        self.emoticons = self.__load_emoticons()

    def preprocess_posts(self, posts: list[Post]) -> None:
        if self.nlp.has_pipe('lemmatizer'):
            self.nlp.remove_pipe('lemmatizer')
        if not self.nlp.has_pipe('emoji'):
            self.nlp.add_pipe('emoji', first=True)

        posts = [self.__process_post(post) for post in posts]
        posts = [post for post in posts if post is not None]

        logging.info('Enlazando entidades de los posts...')
        self.linker.link([''.join(post.text).lower() for post in posts])

        self.__save_posts_to_file(posts, f'{constants.PREPROCESSED_DIRECTORY}/{self.posts_source}/preprocessed_')
    
    def __process_post(self, post: Post) -> Post|None:
        self.__check_language_pipe()
        if not self.__is_post_within_date_range(post):
            return None

        doc = self.nlp(post.text)

        if not doc._.language['language'] == 'en':
            return None

        tokenized_text = [self.__process_token(token, post) for token in doc]
        post.tokenized_text = [token for token in tokenized_text if token != '' and token != None]

        post.text = ' '.join(post.tokenized_text)
        
        return post

    def __process_token(self, token: Token, post: Post) -> str:
        if token.like_url:
            post.urls.add(token.text)
            return ''

        if token.text.startswith('#'):
            post.hashtags.add(token.text)
            return token.text[1:]

        if token.text.startswith('@'):
            post.mentions.add(token.text)
            return ''

        if token._.is_emoji:
            return token._.emoji_desc
        
        if token.text in self.emoticons:
            return self.emoticons[token.text]
        
        if token.text.lower() in self.misspellings:
            return self.misspellings[token.text.lower()]

        #check whether some letter is repeated more than 4 times, if so, reduce it to 2
        text = re.sub(r'([a-zA-Z])\1{4,}', r'\1\1', token.text)
          
        return text
  
    def normalize_posts(self, posts):
        logging.info('Normalizing posts...')
        self.__substitute_entities_by_ids(posts)

        tokenized_posts = self.__tokenize(posts)
        self.__lematize_posts(tokenized_posts)

        logging.info('Saving normalized posts...')
        self.__save_posts_to_file(tokenized_posts, f'{constants.NORMALIZED_DIRECTORY}/{self.posts_source}/normalized_')
    
    def create_lang_detector(self, nlp: Language, name: str) -> LanguageDetector:
        return LanguageDetector()

    def __substitute_entities_by_ids(self, posts: list[Post]) -> None:
        for post in posts:
            post.text = self.linker.substitute_entites_by_ids(post.text)


    def __check_language_pipe(self) -> None:
        if not self.nlp.has_pipe("language_detector"):
            Language.factory("language_detector", func=self.create_lang_detector)
            self.nlp.add_pipe('language_detector', last=True)
    
    def __is_post_within_date_range(self, post: Post) -> bool:
        start = parse(constants.START_DATE)
        end = parse(constants.END_DATE)

        return start <= post.timestamp <= end

    def __lematize_posts(self, tokenized_posts):
        lemmatized_text = []
        for post in tokenized_posts:
            lemmatized_text += [token.lemma_ for token in post.tokenized_text if self.__is_word(token)]
            post.text = ' '.join(lemmatized_text)
            lemmatized_text = []

        return tokenized_posts

    def __save_posts_to_file(self, posts: list[Post], base_filename: str) -> None:
        filename = f'{base_filename}{self.file_counter}.json'
        with open(filename, 'w') as f:
            json.dump([post.to_dict() for post in posts], f, indent=4, default=str)

        self.file_counter += 1
    
    def __load_misspellings(self) -> dict[str, str]:
        misspellings = {}
        with open(constants.MISSPELLINGS_FILE, 'r') as f:
            for row in f:
                # last element is the correct spelling
                misspellings.update({misspelling.strip(): row.split('|')[1].strip() for misspelling in row.split('|')[:-1]})
        return misspellings

    def __load_emoticons(self) -> dict[str, str]:
        emoticons = {}
        with open(constants.EMOTICONS_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t')
            emoticons.update({row['emoticon']: row['description'] for row in reader})
        return emoticons


    def __is_word(self, token: Token) -> bool:
        is_word = True
        
        is_word &= not token.is_stop
        is_word &= not token.is_punct
        is_word &= not token.is_space

        return is_word