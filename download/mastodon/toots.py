import constants
import logging
import csv
from typing import Any
from tootpy import MastodonClient


class TootsClient(MastodonClient):

    def __init__(self) -> None:
        super().__init__()
        self.toots_ids_by_instance = self.__load_toots_ids()
    
    def __load_toots_ids(self) -> dict[str, str]:
        with open(f'{constants.DATA_DIRECTORY}/posts_instances.csv', 'r') as f:
            reader = csv.DictReader(f)
            return {row['id']: row['domain'] for row in reader}
    
    def get_posts(self, ids: list[str]) -> None:
        posts: list[dict[str, Any]] = []
        for id in ids:
            try:
                posts.append(self.__get_post(id))
            except Exception as e:
                logging.error(f'Error fetching post {id}: {e}')
                continue
            
            if len(posts) >= constants.MAX_POSTS_PER_FILE:
                self.save_posts_to_file(posts)
                posts = []
                self.file_counter += 1
        
        self.save_posts_to_file(posts)
    
    def __get_post(self, id: str) -> dict[str, Any]:
        domain = self.toots_ids_by_instance[id]
        client = self.get_api_instance(domain)
        post = client.status(id)

        return post