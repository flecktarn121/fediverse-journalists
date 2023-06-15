import constants
import logging
import csv
from typing import Any
from tootpy import MastodonClient


class TootsClient(MastodonClient):

    def __init__(self) -> None:
        super().__init__()

        #the accounts to which each post belongs
        self.posts_ids_to_accounts_ids = self.__load_dictionary('posts_accounts', 'id', 'domain')
        #the usernames of the previous accounts
        self.accounts_ids_to_usernames= self.__load_dictionary('accounts_ids_usernames', 'id', 'username')
    
    def __load_dictionary(self, filename: str, keyname: str, valuename:str) -> dict[str, str]:
        with open(f'{constants.DATA_DIRECTORY}/{filename}', 'r') as f:
            reader = csv.DictReader(f)
            return {row[keyname]: row[valuename] for row in reader}
    
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
        domain = self.__get_domain(id)
        client = self.get_api_instance(domain)
        post = client.status(id)

        return post
    
    def __get_domain(self, id: str) -> str:
        try:
            account_id = self.posts_ids_to_accounts_ids[id]
            username = self.accounts_ids_to_usernames[account_id]
            return self.parse_domain(username)
        except KeyError:
            raise Exception(f'No account info for post {id}')