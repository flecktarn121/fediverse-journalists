import csv
import logging
import constants
from quotes import QuoteClient 

def load_journalists_from_file(file_path: str) -> list[str]:
    journalists_ids = []
    
    with open(file_path, 'r') as f:
        for row in csv.DictReader(f):
            journalists_ids.append(row['twitter'])
            break
    
    return journalists_ids

def main() -> None:
    logging.basicConfig(
        filename=f'{constants.LOGS_DIRERCTORY}info.log',
        level=logging.INFO, 
        encoding='utf-8')
    
    journalists_ids = load_journalists_from_file(f'{constants.DATA_DIRERCTORY}journalists.csv')
    client = QuoteClient()
    client.retrieve_posts(journalists_ids)

if __name__ == '__main__':
    main()