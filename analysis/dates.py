import os
import ijson
import json
import datetime
from post import Post
from dateutil.parser import parse


def main():
    end_date = datetime.datetime(2022, 10, 26, tzinfo=datetime.timezone.utc)
    for file in os.listdir('data/normalized/twitter'):
        with open(os.path.join('data/normalized/twitter', file), 'r') as f:
            posts = ijson.items(f, 'item')
            posts = [Post.load_from_json(post) for post in posts]
            for post in posts:
                if post.timestamp > end_date:
                    end_date = post.timestamp
    
    print(f'Fecha del último tweet: {end_date}')

    file_counter = 0
    file_counter = process_mastodon_directory('data/normalized/mastodon', file_counter, end_date)
    file_counter = process_mastodon_directory('data/normalized/mastodon/alien', file_counter, end_date)
    file_counter = process_mastodon_directory('data/normalized/mastodon/despacho', file_counter, end_date)

    print(f'Procesados {file_counter} archivos')

def process_mastodon_directory(directory, file_counter, end_date):
    for file in os.listdir(directory):
        if file.endswith('.json'):
            with open(os.path.join(directory, file), 'r') as f:
                posts = ijson.items(f, 'item')
                posts = [Post.load_from_json(post) for post in posts if parse(post['timestamp']) < end_date]
                save_to_json(file_counter, posts)

            file_counter += 1
    
    return file_counter


def save_to_json(file_counter, posts):
    with open(f'data/normalized/mastodon/final/normalized_{file_counter}.json', 'w') as f:
        json.dump([post.to_dict() for post in posts], f, indent=4)


if __name__ == '__main__':
    main()
