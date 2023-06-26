import ijson
import json
import random
import os
from post import Post


def get_random_posts(dir_name):
    random_posts = []
    for file_name in os.listdir(dir_name):
        posts = []
        with open(dir_name + '/' + file_name, 'r', encoding='utf-8') as file:
            posts = json.load(file)
        if len(posts) != 0:
            random_posts.append(random.choice(posts))

    return random_posts

def save_posts(posts, file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(posts, file, indent=4)

if __name__ == '__main__':
    random_mastodon_posts = get_random_posts('data/normalized/mastodon/final')
    save_posts(random_mastodon_posts, 'data/random_mastodon_posts.json')
    random_mastodon_posts = get_random_posts('data/normalized/twitter')
    save_posts(random_mastodon_posts, 'data/random_twitter_posts.json')
    print('Done')