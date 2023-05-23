import csv
import constants
import time
import requests
import json
import logging
from urllib.parse import quote
from entity import Entity

def get_entity_name(entity):
    print(f'Getting label for {entity.name}')
    data = __query_wikidata(constants.WIKIDATA_GET_API, entity.main_match)
    if data is not None and 'entities' in data:
        wikidata_entity = data['entities'][entity.main_match]
        if 'en' in wikidata_entity['labels']:
            entity.label = wikidata_entity['labels']['en']['value']
            print(f'Label is {entity.label}')


def __query_wikidata(url, parameter):
    url_query = quote(parameter)
    response = requests.get(url + url_query)
    data = json.loads(response.text)
    if response.status_code != 200 or 'error' in data:
        logging.error(f'Error while querying wikidata: {response.status_code}')
        return None
    
    time.sleep(2) 
    return data

def load_entities_from_csv():
    entites = []
    with open('analysis/data/entities/entities1_filtered.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            entity = Entity(row['name'])
            entity.frequency = int(row['frequency'])
            entity.main_match = row['main_match']
            entity.description = row['description']
            entity.secondary_matches = row['potenial_matches']
            entites.append(entity)
    
    return entites

def save_entities_to_file(entities):
    print('Saving entities to file')
    with open('analysis/data/entities/labelled_entities.csv', 'w', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['name', 'frequency', 'main_match','label', 'description', 'potenial_matches']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for entity in entities:
            writer.writerow({'name': entity.name, 'frequency': entity.frequency, 'main_match': entity.main_match, 'label':entity.label, 'description': entity.description, 'potenial_matches': entity.secondary_matches})

def main():
    entities = load_entities_from_csv()
    for entity in entities:
        try:
            get_entity_name(entity)
        except Exception:
            pass
    save_entities_to_file(entities)

if __name__ == '__main__':
    main()