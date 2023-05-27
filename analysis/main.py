import os
import ijson
import constants
from preprocessing import PreProcessor
from nel import NamedEntityLinker
from post import Post
import logging


def load_twitter_posts(preprocessor):
    #iterate all the json files in data folder and load the posts in each of of them
    for file in os.listdir(constants.RAW_DIRECTORY_TWITTER):
        with open(os.path.join(constants.RAW_DIRECTORY_TWITTER, file), 'r') as f:
            logging.info(f'Loading file {file}')
            posts = ijson.items(f, 'item')
            posts = [Post.load_twitter_post(post) for post in posts]
            preprocessor.preprocess_posts(posts)

def load_mastodon_posts(preprocessor):
    for file in os.listdir(constants.RAW_DIRECTORY_MASTODON):
        with open(os.path.join(constants.RAW_DIRECTORY_MASTODON, file), 'r') as f:
            logging.info(f'Loading file {file}')
            posts = ijson.items(f, 'item')

            posts = [Post.load_mastodon_post(post) for post in posts]
            preprocessor.preprocess_posts(posts)


def main():
    logging.basicConfig(level=logging.INFO, filename='processing.log')

    preprocessor = PreProcessor()
    try:
        preprocessor.posts_source = 'twitter'
        logging.info('Loading twitter posts')
        #load_twitter_posts(preprocessor)
        preprocessor.posts_source = 'mastodon'
        logging.info('Loading mastodon posts')
        load_mastodon_posts(preprocessor)
        logging.info('Guardando entidades')
        preprocessor.linker.save_entities_to_file()
    except Exception as e:
        logging.error(e)
        
def clean_entities():
    nel = NamedEntityLinker()
    nel.load_entities_from_file('entities.old.csv')
    nel.remove_entites_below_frequency(10)
    nel.save_entities_to_file()

def perform_nel():
    logging.basicConfig(level=logging.INFO, filename='nel.log')
    nel = NamedEntityLinker()
    nel.load_entities_from_file('data/entities/entities.csv')
    nel.retrieve_wikidata_info(list(nel.entities_by_name.values()))
    nel.save_entities_to_file()

def normalize():
    logging.basicConfig(level=logging.INFO, filename='logs/normalize.log')
    nel = NamedEntityLinker()
    nel.load_entities_from_file('data/entities/entities.csv')
    preProcessor = PreProcessor()
    preProcessor.linker = nel
    preProcessor.posts_source = 'mastodon'
    for file in os.listdir(constants.PREPROCESSED_DIRECTORY_MASTODON):
        with open(os.path.join(constants.PREPROCESSED_DIRECTORY_MASTODON, file), 'r') as f:
            logging.info(f'Loading file {file}')
            posts = ijson.items(f, 'item')
            posts = [Post.load_from_json(post) for post in posts]
            preProcessor.normalize_posts(posts)

if __name__ == '__main__':
    normalize()