import mastodon
import logging
import os
import json
from datetime import datetime, timezone


class MastodonClient:

    def __init__(self)-> None:
        self.total_toots_fetched = 0
        self.file_counter = 0

    def  get_posts(self, user_ids: list[str]) -> None:
        for id in user_ids:
            try:
                self.process_user(id)
            except Exception as e:
                pass

    def process_user(self, id: str) -> None:
        pass

    def get_toots_for_account(user_id: str, client: mastodon.Mastodon) -> list[dict]:
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

        logging.info(f'Fetched {len(statuses)} toots of {account["username"]}.')
        return statuses

    def save_posts_to_file(self, replies: list[dict]) -> None:
        file_name = os.path.join('mastodon/data', f'{self.file_counter}.json')

        with open(f'mastodon/data/{file_name}', 'w') as f:
            json.dump(replies, f, default=str)

    def parse_domain(self, acct: str) -> str:
        return acct.split('@')[-1]

    def get_api_instance(self, base_url:str=None) -> mastodon.Mastodon:
        if base_url is None:
            return mastodon.Mastodon(
                client_id=credentials.APP_ID,
                client_secret=credentials.SECRET,
                access_token=credentials.ACCESS_TOKEN,
                api_base_url='https://mastodon.social')
        else:
            return mastodon.Mastodon(api_base_url=base_url)