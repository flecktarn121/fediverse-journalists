import csv
import constants
from typing import Any
from toots import TootsClient
from multiprocessing import Pool, cpu_count
from users import UsersClient

def read_ids_by_instance() -> dict[str, set[str]]:
    users_by_instnace: dict[str, set[str]] = {}
    with open(f'{constants.DATA_DIRECTORY}/journalists.csv', 'r') as f:
        try:
            process_rows(users_by_instnace, f)
        except Exception as e:
            pass

    return users_by_instnace

def process_rows(users_by_instance: dict[str, set[str]], f: Any) -> None:
    reader = csv.DictReader(f)
    for row in reader:
        user = row['mastodon']
        domain = get_domain_from_username(user)
        if domain in users_by_instance:
            users_by_instance[domain].add(user)
        else:
            users_by_instance[domain] = set([user])

def get_domain_from_username(username: str) -> str:
    return username.split('@')[-1]

def get_posts(ids) -> None:
    client = TootsClient()
    client.get_posts(ids)

def main() -> None:
    journalists_by_domain = read_ids_by_instance()
    posts_ids = journalists_by_domain.values()
    pool = Pool(cpu_count())
    pool.map(get_posts, posts_ids)
    '''
    with open(f'{constants.DATA_DIRECTORY}/journalists.csv', 'r') as f:
        usernames = [row['mastodon'] for row in csv.DictReader(f)]

    client = UsersClient()
    client.get_posts(usernames)
    '''


if __name__ == '__main__':
    main()