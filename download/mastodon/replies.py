import mastodon
from datetime import datetime, timezone
import credentials
import logging
import json
import random


def get_replies(journalists_ids):
    total_toots_fetched = 0

    for id in journalists_ids:
        try:
            process_journalist(total_toots_fetched, id)
        except Exception as e:
            pass

def process_journalist(total_toots_fetched, id):
    client = get_api_instance()
    current_date = datetime.now()
    configure_logging(id)
    logging.info(f'Fetching replies for {id} at {current_date}...')

    replies = get_replies_for_journalist(id, client)
    total_toots_fetched += len(replies)

    logging.info(f'A total of {total_toots_fetched} toots have been retrieved so far...')
    save_replies_to_file(replies, total_toots_fetched)

def get_replies_for_journalist(journalist_id, client):
    logging.info(f'Fetching replies for {journalist_id}...')
    replies = []
    domain = parse_domain(journalist_id)
    client = get_api_instance(base_url=f'https://{domain}')

    try:
        account = client.account_lookup(journalist_id)
        toots = get_toots(account, client)
        replies = get_replies_for_toots(toots, client)
    except mastodon.errors.MastodonNotFoundError:
        logging.error(f'Journalist {journalist_id} not found.')
    except Exception as e:
        logging.error(f'Error fetching replies for journalist {journalist_id}: {e}')
    
    logging.info(f'Fetched {len(replies)} replies for journalist {journalist_id}.')
    return replies

def get_toots(account, client):
    logging.info(f'Fetching toots of {account["username"]}...')
    begin_date = datetime(2022, 10, 26, tzinfo=timezone.utc)
    statuses = []

    fetched_statuses = client.account_statuses(account, exclude_reblogs=True, limit=40)
    filtered_statuses = [status for status in fetched_statuses if status['created_at'] > begin_date]

    statuses += filtered_statuses

    if len(fetched_statuses) != len(filtered_statuses):
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

def get_replies_for_toots(toots, client):
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

def save_replies_to_file(replies, toots_retrieved):
    file_name = str(random.randint(1, 100000)) + '_' + str(toots_retrieved) + '.json'

    with open(f'mastodon/data/{file_name}', 'w') as f:
        json.dump(replies, f, default=str)

def parse_domain(acct):
    return acct.split('@')[-1]

def get_api_instance(base_url=None):
    if base_url is None:
        return mastodon.Mastodon(
            client_id=credentials.APP_ID,
            client_secret=credentials.SECRET,
            access_token=credentials.ACCESS_TOKEN,
            api_base_url='https://mastodon.social')
    else:
        return mastodon.Mastodon(api_base_url=base_url)

def configure_logging(id):
    username = id.split('@')[1]
    logging.basicConfig(
        filename=f'mastodon/logs/{username}.log',
        level=logging.INFO, 
        encoding='utf-8')