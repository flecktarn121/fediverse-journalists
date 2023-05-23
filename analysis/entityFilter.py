import csv
import time
from entity import Entity


def load_entities_from_csv():
    entites = []
    with open('data/entities/labelled_entities.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        counter = 0
        for row in reader:
            entity = Entity(row['name'])
            entity.frequency = int(row['frequency'])
            entity.main_match = row['main_match']
            entity.description = row['description']
            entity.secondary_matches = row['potenial_matches']
            entity.label = row['label']
            entites.append(entity)
            counter += 1
    
    return entites

def filter_entities(entities):
    filtered_entities = []
    forbidden_words = {'song', 'album', 'single', 'film', 'movie'}
    counter = 0
    for entity in entities:
        description_words = set(entity.description.split())
        filtered_entities.append(entity)
        counter += 1
    return filtered_entities

def save_entities_to_file(entities, filename):
    entities.sort(key=lambda x: x.frequency, reverse=True)
    with open(filename, 'w', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['name', 'frequency', 'main_match', 'label', 'description', 'potenial_matches']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for entity in entities:
            if entity.main_match != '' and entity.label != '':
                writer.writerow({'name': entity.name, 'frequency': entity.frequency, 'main_match': entity.main_match, 'label':entity.label, 'description': entity.description, 'potenial_matches': entity.secondary_matches})

if __name__ == "__main__":
    #sleep for 2 hours
    time.sleep(7200)
    entities = load_entities_from_csv()
    #filtered_entities = filter_entities(entities)
    save_entities_to_file(entities, 'data/entities/entities.csv')
