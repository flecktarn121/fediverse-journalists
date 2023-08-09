import logging
import csv
import time
import requests
import json
import logging
from urllib.parse import quote
import sys
sys.path.append('analysis')
import constants
from entity import Entity

def get_entity_name(entity: Entity):
    logging.info(f'Getting label for {entity.name}')
    data = __query_wikidata(constants.WIKIDATA_GET_API, entity.main_match)
    if data is not None and 'entities' in data:
        wikidata_entity = data['entities'][entity.main_match]
        if 'en' in wikidata_entity['labels']:
            entity.label = wikidata_entity['labels']['en']['value']
            entity.description = wikidata_entity['descriptions']['en']['value'] if 'en' in wikidata_entity['descriptions'] and wikidata_entity['descriptions']['en'] else ''
            logging.info(f'Label is {entity.label}')
            time.sleep(4) 


def __query_wikidata(url, parameter):
    url_query = quote(parameter)
    response = requests.get(url + url_query)
    data = json.loads(response.text)
    if response.status_code != 200 or 'error' in data:
        logging.error(f'Error while querying wikidata: {response.status_code}')
        return None
    
    time.sleep(2) 
    return data

def load_entities_from_csv() -> list[Entity]:
    entites = []
    with open('analysis/data/entities/entities.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            entity = Entity(row['name'])
            entity.label = row['label']
            entity.frequency = int(row['frequency'])
            entity.main_match = row['main_match']
            entity.description = row['description']
            entity.secondary_matches = row['potenial_matches']
            entites.append(entity)
    
    return entites

def save_entities_to_file(entities: list[Entity]) -> None:
    logging.info('Saving entities to file')
    with open('analysis/data/entities/labelled_entities.csv', 'w', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['name', 'frequency', 'main_match','label', 'description', 'potenial_matches']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for entity in entities:
            writer.writerow({'name': entity.name, 'frequency': entity.frequency, 'main_match': entity.main_match, 'label':entity.label, 'description': entity.description, 'potenial_matches': entity.secondary_matches})

def main():
    logging.basicConfig(level=logging.INFO, filename=f'{constants.LOGGING_DIRECTORY}/wikidata.log')
    entities = load_entities_from_csv()
    for entity in entities:
        try:
            if entity.label == '':
                get_entity_name(entity)
        except Exception:
            logging.error(f'Error while getting label for {entity.name}')
            continue
    save_entities_to_file(entities)

if __name__ == '__main__':
    main()