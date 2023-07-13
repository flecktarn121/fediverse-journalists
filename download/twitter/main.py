import csv
import logging
import constants
from tweet import TweetClient

def load_journalists_from_file(file_path: str) -> list[str]:
    journalists_ids = []
    
    with open(file_path, 'r') as f:
        for row in csv.DictReader(f):
            journalists_ids.append(row['twitter'])
    
    return journalists_ids

def main() -> None:

    print('Have you set all the parameters? (y/n)')
    answer = input()
    if answer.lower() != 'y':
        print('Please set the parameters and try again.')
        exit()

    logging.basicConfig(
        filename=f'{constants.LOGS_DIRERCTORY}info.log',
        level=logging.INFO, 
        encoding='utf-8')
    
    journalists_ids = load_journalists_from_file(f'{constants.DATA_DIRERCTORY}journalists.csv')
    client = TweetClient(posts_retrieved=1_901_753)
    client.retrieve_posts(journalists_ids)

if __name__ == '__main__':
    main()