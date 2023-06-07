import csv
import logging
import constants
from replies import TwitterClient


def load_journalists_from_file(file_path):
    journalists_ids = []
    
    with open(file_path, 'r') as f:
        for row in csv.DictReader(f):
            journalists_ids.append(row['twitter_handle'])
    
    return journalists_ids

def main():
    logging.basicConfig(
        filename='info.log',
        level=logging.INFO, 
        encoding='utf-8')
    
    journalists_ids = load_journalists_from_file(f'{constants.DESTINATION_DIRERCTORY}journalists.csv')
    client = TwitterClient()
    client.__retrieve_posts(journalists_ids)

if __name__ == '__main__':
    main()