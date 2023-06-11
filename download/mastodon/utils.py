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

            domain = urlparse(status['url']).hostname
            if status['in_reply_to_id'] is None:
                continue
            if status['in_reply_to_id'] not in posts_instances:
                posts_instances[status['in_reply_to_id']] = domain


if __name__ == '__main__':
    posts_instances = main()
    with open(f'{constants.DATA_DIRECTORY}/posts_instances.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'domain'])
        for key, value in posts_instances.items():
            writer.writerow([key, value])