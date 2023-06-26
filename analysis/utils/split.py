import os
import ijson
import json

def split():
    filenames = os.listdir('data/raw/mastodon')
    for filename in filenames:
        if filename.endswith('.json'):
            with open(f'data/raw/mastodon/{filename}', 'r') as f:
                counter = 0
                filename_counter = 0
                posts = []
                for post in ijson.items(f, 'item'):
                    posts.append(post)
                    counter += 1
                    if counter == 1000:
                        with open(f'data/split/mastodon/{filename}{filename_counter}.json', 'w') as outfile:
                            json.dump(posts, outfile, indent=4, default=str)
                        counter = 0
                        posts = []
                        filename_counter += 1
                with open(f'data/split/mastodon/{filename}{filename_counter}.json', 'w') as outfile:
                    json.dump(posts, outfile, indent=4, default=str)


if __name__ == '__main__':
    split()