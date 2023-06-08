import json
import logging
from tootpy import MastodonClient


class TootsClient(MastodonClient):

    def __init__(self) -> None:
        super().__init__()
        self.toots_ids_by_user = self.__load_toots_ids()
        self.users_instances = self.__load_users_instances()
    
    def __load_toots_ids(self) -> dict[str, list[str]]:
        with open('mastodon/data/toots_ids.json', 'r') as f:
            return json.load(f)
    
    def __load_users_instances(self) -> dict[str, str]:
        with open('mastodon/data/users_instances.json', 'r') as f:
            return json.load(f)
    
    def process_user(self, id: str) -> None:
        instance_url = self.users_instances[id]
        client = self.get_api_instance(instance_url)

        toots_ids = self.toots_ids_by_user[id]
        for toot_id in toots_ids:
            try:
                client.status(toot_id)
            except Exception as e:
                logging.error(f'Error fetching toot {toot_id} of user {id}: {e}')
