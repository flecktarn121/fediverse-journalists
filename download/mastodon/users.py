import logging
import csv
import constants
import os
from tootpy import MastodonClient

class UsersClient(MastodonClient):

    def process_user(self, id: str) -> None:
        try:
            self.__process_user(id)
        except Exception as e:
            logging.error(f'Error processing user {id}: {e}')
    
    def __process_user(self, id: str) -> None:
        domain = self.parse_domain(id)
        client = self.get_api_instance(domain)
        user = client.account_lookup(id)

        self.__save_to_file(id, user['id'])

    def __save_to_file(self, username: str, internal_id: int) -> None:
        file_name = os.path.join(constants.DATA_DIRECTORY, 'accounts_ids_usernames.csv')

        with open(file_name, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if self.file_counter == 0:
                writer.writerow(['id', 'username'])
            writer.writerow([internal_id, username])

            self.file_counter += 1

