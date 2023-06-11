from typing import Any
import random
import constants
import credentials
import logging
import os
import json
from mastodon import Mastodon # type: ignore
from datetime import datetime, timezone


class MastodonClient:

    def __init__(self)-> None:
        self.total_toots_fetched = 0
        self.file_counter = 0

        random_indentifier = random.randint(0, 1000000)
        self.file_prefix = f'masto_{random_indentifier}_'

        log_file_name = f'{constants.LOGS_DIRECTORY}/masto_{random_indentifier}.log'
        logging.basicConfig(
            filename=log_file_name, 
            level=logging.INFO)


    def  get_posts(self, ids: list[str]) -> None:
        for id in ids:
            try:
                self.process_user(id)
            except Exception as e:
                pass

    def process_user(self, id: str) -> None:
        pass

    def get_toots_for_account(self, user_id: str, client: Mastodon) -> list[dict]:
        account = client.account_lookup(user_id)

        logging.info(f'Fetching toots of {account["username"]}...')
        begin_date = datetime(2022, 10, 26, tzinfo=timezone.utc)
        statuses = []

        fetched_statuses = client.account_statuses(account, exclude_reblogs=True, limit=40)
        filtered_statuses = [status for status in fetched_statuses if status['created_at'] > begin_date]

        statuses += filtered_statuses

        if len(fetched_statuses) != len(filtered_statuses): #the begin date has been reached
            return statuses

        while True:
            if not hasattr(fetched_statuses, '_pagination_next'):
                break
            try:
                fetched_statuses = client.fetch_next(fetched_statuses._pagination_next)
            except Exception as e:
                logging.error(f'Error fetching toots of {account["username"]}: {e}')
                break

            filtered_statuses = [status for status in fetched_statuses if status['created_at'] > begin_date]
            statuses += filtered_statuses
            if len(fetched_statuses) != len(filtered_statuses):
                break

        logging.info(f'Fetched {len(statuses)} posts of {account["username"]}.')
        return statuses

    def save_posts_to_file(self, replies: list[dict[str, Any]]) -> None:
        file_name = os.path.join(constants.DATA_DIRECTORY, f'{self.file_prefix}{self.file_counter}.json')

        with open(file_name, 'w') as f:
            json.dump(replies, f, default=str)

    def parse_domain(self, acct: str) -> str:
        return acct.split('@')[-1]

    def get_api_instance(self, base_url:str|None=None) -> Mastodon:
        if base_url is None:
            return Mastodon(
                client_id=credentials.APP_ID,
                client_secret=credentials.SECRET,
                access_token=credentials.ACCESS_TOKEN,
                api_base_url='https://mastodon.social',
                )
        else:
            return Mastodon(api_base_url=base_url)