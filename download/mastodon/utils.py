import constants
import os
import ijson # type: ignore
import csv
from typing import TextIO
from urllib.parse import urlparse
from dateutil.parser import parse


def main() -> dict[str, str]:
    posts_instances: dict[str, str] = {}
    directory = f'{constants.DATA_DIRECTORY}/raw'
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(f'{directory}/{filename}', 'r') as f:
                processFile(posts_instances, f)
    
    return posts_instances

def processFile(posts_instances: dict[str, str], f: TextIO ) -> None:
        end_date = parse('2023-03-28T19:43:22Z')
        statuses = ijson.items(f, 'item')
        for status in statuses:
            if parse(status['created_at']) > end_date:
                continue

            if status['in_reply_to_id'] is None:
                continue
            if status['in_reply_to_id'] not in posts_instances:
                posts_instances[status['in_reply_to_id']] = status['in_reply_to_account_id']

def join_dictionaries() -> None:
    posts_ids_to_user_ids: dict[str, str] = {}
    with open(f'{constants.DATA_DIRECTORY}/posts_accounts.csv', 'r') as f:
        reader = csv.DictReader(f)
        posts_ids_to_user_ids = {row['id']: row['account'] for row in reader}
    
    user_ids_to_usernames: dict[str, str] = {}
    with open(f'{constants.DATA_DIRECTORY}/accounts_ids_usernames.csv', 'r') as f:
        reader = csv.DictReader(f)
        user_ids_to_usernames = {row['id']: row['username'] for row in reader}
    
    posts_ids_to_usernames: dict[str, str] = {}
    for post_id, user_id in posts_ids_to_user_ids.items():
        if user_id in user_ids_to_usernames:
            posts_ids_to_usernames[post_id] = user_ids_to_usernames[user_id]
    
    with open(f'{constants.DATA_DIRECTORY}/posts_ids_usernames.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'username'])
        for post_id, username in posts_ids_to_usernames.items():
            writer.writerow([post_id, username])

if __name__ == '__main__':
    '''
    posts_instances = main()
    with open(f'{constants.DATA_DIRECTORY}/posts_accounts.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'account'])
        for key, value in posts_instances.items():
            writer.writerow([key, value])
    '''
    join_dictionaries()