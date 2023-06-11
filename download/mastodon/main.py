import csv
import constants
from typing import Any
from toots import TootsClient
from multiprocessing import Pool, cpu_count

def read_ids_by_instance() -> dict[str, set[str]]:
    post_ids_by_instance: dict[str, set[str]] = {}
    with open(f'{constants.DATA_DIRECTORY}/posts_to_instances.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['domain'] not in post_ids_by_instance:
                post_ids_by_instance[row['domain']] = set()
            post_ids_by_instance[row['domain']].add(row['id']) 

    return post_ids_by_instance

def process_row(journalists_by_domain: dict, f: Any) -> None:
    reader = csv.reader(f)
    for row in reader:
        user = row[2]
        domain = get_domain_from_username(user)
        if domain in journalists_by_domain:
            journalists_by_domain[domain].append(row[2])
        else:
            journalists_by_domain[domain] = [row[2]]

def get_domain_from_username(username: str) -> str:
    return username.split('@')[-1]

def get_posts(ids) -> None:
    client = TootsClient()
    client.get_posts(ids)

def main() -> None:
    journalists_by_domain = read_ids_by_instance()
    # get the values of the dictionary
    posts_ids = journalists_by_domain.values()
    pool = Pool(cpu_count())
    pool.map(get_posts, posts_ids)

if __name__ == '__main__':
    main()