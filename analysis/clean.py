import os
import ijson
import json
import spacy
import constants
import textacy
from post import Post
from multiprocessing import Pool, cpu_count


def load_posts(filename):
    posts = []
    nlp = spacy.load(constants.SPACY_MODEL)
    with open(filename, 'r', encoding='utf-8') as file:
        posts = ijson.items(file, 'item')
        posts = [Post.load_from_json(post) for post in posts]
        process_posts(posts, nlp)
        

    with open(filename, 'w', encoding='utf-8') as file:
        json.dump([post.to_dict() for post in posts], file, indent=4)

def process_posts(posts, nlp):
    for post in posts:
        post.tokenized_text = [token for token in post.text.split(' ') if is_valid_token(token)]
        post.text = ' '.join(post.tokenized_text)
        post.entities = set()
        doc = nlp(post.text)
        post.entities.update([entity.text for entity in doc.ents])
        post.entities.update([chunk.text for chunk in doc.noun_chunks])


def is_valid_token(token):
    is_valid = True

    #is_valid &= not 'http' in token
    #is_valid &= not '@' in token
    #is_valid &= not 'tag' in token

    return is_valid

if __name__ == '__main__':
    pool = Pool(processes=cpu_count())
    directory = constants.NORMALIZED_DIRECTORY + '/twitter'
    pool.map(load_posts, [f'{directory}/{filename}' for filename in os.listdir(directory)])

    directory = constants.NORMALIZED_DIRECTORY + '/mastodon/final'
    pool.map(load_posts, [f'{directory}/{filename}' for filename in os.listdir(directory)])

