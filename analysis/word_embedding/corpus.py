import ijson #type: ignore
import os
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import constants


def get_corpus_from_directory(directory: str) -> str:
    corpus = ""
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            with open(os.path.join(directory, filename), "r") as f:
                posts = ijson.items(f, "item")
                texts = [post["text"] + '\n' for post in posts]
                corpus += ' '.join(texts)
    return corpus

def save_corpus_to_file(filename: str, corpus: str) -> None:
    with open(f'{constants.CORPUS_DIRECTORY}/{filename}', "w", encoding='utf-8') as f:
        f.write(corpus)

def get_corpus_from_file(filename: str) -> str:
    with open(filename, "r", encoding='utf-8') as f:
        return f.read()

def main() -> None:
    print('Loading twitter corpus')
    corpus = get_corpus_from_directory(constants.NORMALIZED_DIRECTORY + '/twitter')
    print('Saving twitter corpus')
    save_corpus_to_file('twitter_corpus.txt', corpus)

    print('Loading mastodon corpus')
    corpus = get_corpus_from_directory(constants.NORMALIZED_DIRECTORY + '/mastodon')
    print('Saving mastodon corpus')
    save_corpus_to_file('mastodon_corpus.txt', corpus)

    print('Done')

if __name__ == '__main__':
    main()