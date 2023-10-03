import spacy
import csv
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import constants


def load_lexicon(filename: str) -> list[str]:
    with open(filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        return [row[0] for row in reader]

def load_entities(filename: str) -> dict[str, str]:
    with open(filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return {row['name']: row['label'] for row in reader}

def link_words(lexicon: list[str], entities: dict[str, str]) -> list[str]:
    new_lexicon: list[str] = []
    for word in lexicon:
        word = word if word not in entities else entities[word]
        new_lexicon.append(word)
    
    return new_lexicon

def normalize_lexicon(lexicon: list[str]) -> list[str]:
    nlp = spacy.load(constants.SPACY_MODEL)
    normalized_lexicon: list[str] = []
    for word in lexicon:
        doc = nlp(word)
        normalized_lexicon.append(doc[0].lemma_)

    return normalized_lexicon

def save_lexicon(lexicon: list[str], filename: str) -> None:
    with open(filename, 'w', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for word in lexicon:
            writer.writerow([word])
    
def main() -> None:
    lexicon = load_lexicon(constants.RESOURCES_DIRECTORY + '/en.txt')
    entities = load_entities(constants.ENTITIES_FILE)
    lexicon = link_words(lexicon, entities)
    lexicon = normalize_lexicon(lexicon)
    save_lexicon(lexicon, constants.RESOURCES_DIRECTORY + '/profanities.csv')

if __name__ == '__main__':
    main()