import logging
import mastodon
from tootpy import MastodonClient
from datetime import datetime, timezone


class RepliesClient(MastodonClient):

    def process_user(self, id: str) -> None:
        client = self.get_api_instance()
        current_date = datetime.now()
        logging.info(f'Fetching replies for {id} at {current_date}...')

        replies = self.get_replies_for_user(id, client)
        self.total_toots_fetched += len(replies)

        logging.info(f'A total of {self.total_toots_fetched} toots have been retrieved so far...')
        self.save_posts_to_file(replies)

    def get_replies_for_user(self, user_id: str, client):
        logging.info(f'Fetching replies for {user_id}...')
        replies = []
        domain = self.parse_domain(user_id)
        client = self.get_api_instance(base_url=f'https://{domain}')

        try:
            toots = self.get_toots_for_account(user_id, client)
            replies = self.get_replies_for_toots(toots, client)
        except mastodon.errors.MastodonNotFoundError:
            logging.error(f'Journalist {user_id} not found.')
        except Exception as e:
            logging.error(f'Error fetching replies for journalist {user_id}: {e}')
        
        logging.info(f'Fetched {len(replies)} replies for journalist {user_id}.')
        return replies

    def get_replies_for_toots(toots: list[dict], client: mastodon.Mastodon) -> list[dict]:
        replies = []
        replies_ids = []
        processed_toots = 0
        logging.info(f'Fetching replies for {len(toots)} toots of {toots[0]["account"]["username"]}')
        for toot in toots:
            try:
                replies_ids += client.status_context(toot)['descendants']
                replies += [client.status(reply_id) for reply_id in replies_ids]
                processed_toots += 1
            except Exception as e:
                logging.error(f'Error fetching replies for journalist: {e}')
            
            logging.info(f'Processed {processed_toots} / {len(toots)} of {toots[0]["account"]["username"]}.')

        return replies
