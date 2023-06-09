import os
import json
import ijson


def main():
    posts_ids_by_user = {}
    for filename in os.listdir('download/twitter/data/raw'):
        if filename.endswith('.json'):
            with open(f'download/twitter/data/raw/{filename}', 'r') as f:
                processFile(posts_ids_by_user, f)
    
    return posts_ids_by_user

def processFile(posts_ids_by_user, f):
        tweets = ijson.items(f, 'item')
        for tweet in tweets:
            if 'conversation_id' in tweet:
                if tweet['conversation_id'] not in posts_ids_by_user:
                    posts_ids_by_user[tweet['conversation_id']] = []
                posts_ids_by_user[tweet['conversation_id']].append(tweet['id'])

if __name__ == '__main__':
    posts_ids_by_user = main()
    with open('download/twitter/data/tweets_ids_by_user.json', 'w') as f:
        json.dump(posts_ids_by_user, f)