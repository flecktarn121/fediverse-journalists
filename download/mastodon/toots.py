import constants
import logging
import json
import os
from typing import Any
from tootpy import MastodonClient
from dateutil.parser import parse


class TootsClient(MastodonClient):

    def get_posts(self, ids: list[str]) -> None:
        posts: list[dict[str, Any]] = []
        end_date = parse(constants.END_DATE)
        for id in ids:
            retrieved_posts = self.process_user(id)
            posts.extend([post for post in retrieved_posts if post['created_at'] <= end_date])
            
            if len(posts) >= constants.MAX_POSTS_PER_FILE:
                self.save_posts_to_file(posts)
                posts = []
                self.file_counter += 1
        
        self.save_posts_to_file(posts)
    
    def process_user(self, id: str) -> list[dict[str, Any]]:
        posts: list[dict[str, Any]] = []

        try:
            domain = self.parse_domain(id)
            client = self.get_api_instance(domain)
            posts = self.get_toots_for_account(id, client)
        except Exception as e:
            logging.error(f'Error fetching posts of {id}: {e}')

        return posts
    
    def save_posts_to_file(self, replies: list[dict[str, Any]]) -> None:
        file_name = os.path.join(constants.DATA_DIRECTORY + '/toots', f'{self.file_prefix}{self.file_counter}.json')

        with open(file_name, 'w') as f:
            json.dump(replies, f, default=str)
