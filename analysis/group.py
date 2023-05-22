import csv


def group_entities():
    entities = {}
    load_entities_from_file('data/entities/entities_twitter.csv', entities)
    load_entities_from_file('data/entities/entities_mastodon1.csv', entities)
    load_entities_from_file('data/entities/entities_mastodon2.csv', entities)
    load_entities_from_file('data/entities/entities_mastodon3.csv', entities)

    save_to_file(entities, 'data/entities/entities.csv')

def load_entities_from_file(filename, entities):
    with open(filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            entity_name = row['name']
            entity_frequency = int(row['frequency'])
            if entity_name in entities:
                entities[entity_name] += entity_frequency
            else:
                entities[entity_name] = entity_frequency

def save_to_file(entities, filename):
    #sort the dictionary by descending frequency
    entities = {k: v for k, v in sorted(entities.items(), key=lambda item: item[1], reverse=True)}
    with open(filename , 'w', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['name', 'frequency', 'main_match', 'description', 'potenial_matches']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        counter = 0
        for entity_name in entities:
            if entities[entity_name] > 10 and 'http' not in entity_name:
                writer.writerow({'name': entity_name, 'frequency': entities[entity_name], 'main_match': '', 'description': '', 'potenial_matches': ''})
                counter += 1
            if counter == 14000:
                break

if __name__ == "__main__":
    group_entities()