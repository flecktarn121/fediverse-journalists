import csv
from entity import Entity


def load_entities_from_csv():
    entites = []
    with open('data/entities/entities1_filtered.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            entity = Entity(row['name'])
            entity.frequency = int(row['frequency'])
            entity.main_match = row['main_match']
            entity.description = row['description']
            entity.potential_matches = row['potenial_matches']
            entites.append(entity)
    
    return entites

def load_stopwords(filename):
    stopwords = set()
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            stopwords.add(line.strip().lower())
    return stopwords

def filter_entities(entities, stopwords):
    filtered_entities = []
    forbidden_words = ['song', 'album', 'single', 'film', 'movie']
    for entity in entities:
        if entity.name.lower() not in stopwords and entity.description.lower() not in forbidden_words:
            filtered_entities.append(entity)
    return filtered_entities

def save_entities_to_file(entities, filename):
    with open(filename, 'w', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['name', 'frequency', 'main_match', 'description', 'potenial_matches']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for entity in entities:
            writer.writerow({'name': entity.name, 'frequency': entity.frequency, 'main_match': entity.main_match, 'description': entity.description, 'potenial_matches': entity.secondary_matches})

if __name__ == "__main__":
    entities = load_entities_from_csv()
    stopwords = load_stopwords('data/stopwords.txt')
    filtered_entities = filter_entities(entities, stopwords)
    save_entities_to_file(filtered_entities, 'data/entities/.csv')
