START_DATE='2022-10-26T00:00:00Z'
END_DATE='2023-03-28T19:43:22Z'
LOGGING_DIRECTORY = 'analysis/logs'
RAW_DIRECTORY_TWITTER = 'analysis/data/raw/twitter'
RAW_DIRECTORY_MASTODON= 'analysis/data/raw/mastodon'
PREPROCESSED_DIRECTORY_MASTODON= 'analysis/data/preprocessed/mastodon'
PREPROCESSED_DIRECTORY_TWITTER= 'analysis/data/preprocessed/twitter'
PREPROCESSED_DIRECTORY = 'analysis/data/preprocessed'
NORMALIZED_DIRECTORY = 'analysis/data/normalized'
FREQUENCIES_DIRECTORY = 'analysis/data/frequencies'
CORPUS_DIRECTORY = 'analysis/data/corpus'
ENTITIES_FILE = 'analysis/data/entities/entities.csv'
HEDOMETER_LEXICON = 'analysis/data/hedometer/polarizing_words.csv'
COMMON_WORDS = 'analysis/data/hedometer/count_1w.txt'
MISSPELLINGS_FILE = 'analysis/resources/Test_Set_3802_Pairs.txt'
EMOTICONS_FILE = 'analysis/resources/wikipedia_emoticons.tsv'
SPACY_MODEL = 'en_core_web_sm'
WIKIDATA_API_URL = 'https://www.wikidata.org/w/api.php?action=wbsearchentities&language=en&format=json&search='
WIKIDATA_GET_API = 'https://www.wikidata.org/w/api.php?action=wbgetentities&sites=enwiki&languages=en&format=json&ids='
NUM_CLUSTERS = 150
ROUNDING_TIME = 60 #1 day