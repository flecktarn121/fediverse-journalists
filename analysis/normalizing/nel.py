import spacy
import logging
import textacy
import json
import requests
import time
import constants
import csv
from urllib.parse import quote
from entity import Entity
from multiprocessing import Pool, cpu_count


class NamedEntityLinker:

    def __init__(self):
        self.nlp = spacy.load(constants.SPACY_MODEL)
        self.entities_by_name = {}

    def link(self, posts):
        entities = sum([self.__get_entities(post) for post in posts], [])
        self.__update_entity_frequencies(entities)

    def load_entities_from_file(self, filename):
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                entity = Entity(row['name'])
                entity.frequency = int(row['frequency'])
                entity.main_match = row['main_match']
                entity.label = row['label']
                self.entities_by_name[entity.name] = entity

    def remove_entites_below_frequency(self, frequency):
        self.entities_by_name = {key: value for key, value in self.entities_by_name.items() if value.frequency >= frequency}
    
    def substitute_entites_by_ids(self, post_text):
        entities_in_post = self.__get_entities(post_text)
        for entity in entities_in_post:
            name = entity.name.lower()
            if name in self.entities_by_name:
                label = self.entities_by_name[name].label
                post_text = post_text.replace(entity.name, label)
        
        return post_text
    
    def __get_entities(self, post):
        doc = self.nlp(post)
        named_entities = textacy.extract.basics.entities(doc)
        noun_chunks = textacy.extract.basics.noun_chunks(doc)
        acronyms = textacy.extract.acros.acronyms(doc)
        keyterms = textacy.extract.keyterms.textrank(doc)

        entities = set()
        entities.update([entity.text for entity in named_entities])
        entities.update([entity.text for entity in noun_chunks])
        entities.update([entity.text for entity in acronyms])
        entities.update([entity[0] for entity in keyterms])

        return [Entity(entity) for entity in entities]

    def __update_entity_frequencies(self, entities):
        for entity in entities:
            if entity.name not in self.entities_by_name:
                self.entities_by_name[entity.name] = entity

            self.entities_by_name[entity.name].frequency += 1

    
    def retrieve_wikidata_info(self, entities):
        logging.info('Getting info from wikidata')
        for entity in entities:
            logging.info(f'Getting info for {entity.name}')
            data = self.__query_wikidata(constants.WIKIDATA_API_URL, entity.name)

            if (data is not None and len(data['search']) > 0):
                potential_id = data['search'][0]['id']
                data = self.__query_wikidata(constants.WIKIDATA_GET_API, potential_id)
                if data is not None:
                    wikidata_entity = data['entities'][potential_id]
                    self.__process_wikidata_entity(entity, wikidata_entity)
    
    def save_entities_to_file(self):
        logging.info('Saving entities to file')
        entities = list(self.entities_by_name.values())
        with open(constants.ENTITIES_FILE, 'w', encoding='utf-8', newline='') as csvfile:
            fieldnames = ['name', 'frequency', 'main_match', 'description', 'potenial_matches']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for entity in entities:
                writer.writerow({'name': entity.name, 'frequency': entity.frequency, 'main_match': entity.main_match, 'description': entity.description, 'potenial_matches': entity.secondary_matches})


    def __query_wikidata(self, url, parameter):
        url_query = quote(parameter)
        response = requests.get(url + url_query)
        data = json.loads(response.text)
        if response.status_code != 200 or 'error' in data:
            logging.error(f'Error while querying wikidata: {response.status_code}')
            return None
        
        time.sleep(2) 
        return data
    
    def __process_wikidata_entity(self, entity, wikidata_entity):
        if 'en' not in wikidata_entity['labels']:
            return
        
        potential_names = [wikidata_entity['labels']['en']['value'].lower()]
        if len(wikidata_entity['aliases']) > 0 and 'en' in wikidata_entity['aliases']:
            potential_names += [name['value'].lower() for name in wikidata_entity['aliases']['en']]

        if entity.name.lower() in potential_names:
            entity.main_match = wikidata_entity['id']
            entity.description = wikidata_entity['descriptions']['en']['value'] if 'en' in wikidata_entity['descriptions'] else ''
        else:
            entity.secondary_matches.add(wikidata_entity['id'])


