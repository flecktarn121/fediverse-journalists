import ijson #type: ignore
import os
import sys
sys.path.append('..')
import constants


def get_corpus_from_directory(directory: str) -> str:
    corpus = ""
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            with open(os.path.join(directory, filename), "r") as f:
                posts = ijson.items(f, "item")
                texts = [post["text"] for post in posts]
                corpus += ' '.join(texts)
    return corpus

def save_corpus_to_file(filename: str) -> None:
    with open(filename, "w") as f:
        f.write(f'{constants.CORPUS_DIRECTORY}/{filename}')

def get_corpus_from_file(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()