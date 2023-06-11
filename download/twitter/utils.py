import os
import json
import ijson
import constants
from typing import TextIO


def main() -> dict[str, list[str]]:
    posts_ids_by_user: dict[str, list[str]] = {}
    for filename in os.listdir(constants.DATA_DIRERCTORY):
        if filename.endswith('.json'):
            with open(f'{constants.DATA_DIRERCTORY}{filename}', 'r') as f:
                processFile(posts_ids_by_user, f)
    
    return posts_ids_by_user

def processFile(posts_ids_by_user: dict[str, list[str]], f: TextIO ) -> None:
        tweets = ijson.items(f, 'item')
        for tweet in tweets:
            if 'conversation_id' in tweet:
                if tweet['conversation_id'] not in posts_ids_by_user:
                    posts_ids_by_user[tweet['conversation_id']] = []
                posts_ids_by_user[tweet['conversation_id']].append(tweet['id'])

if __name__ == '__main__':
    posts_ids_by_user = main()
    with open(f'{constants.DATA_DIRERCTORY}tweets_ids_by_user.json', 'w') as f:
        json.dump(posts_ids_by_user, f)