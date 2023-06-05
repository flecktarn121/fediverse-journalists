import tweepy
import logging
import credentials
import json
import random
import datetime



def get_replies(journalists_ids):
    current_date = datetime.datetime.now()
    logging.info(f'Fetching replies for journalists started at {current_date}...')

    total_replies = {}
    tweets_retrieved = 0
    for journalist_id in journalists_ids:
        replies = get_replies_for_journalist(journalist_id)
        tweets_retrieved += len(replies)
        save_replies_to_file(replies, tweets_retrieved)
        logging.info(f'A total of {tweets_retrieved} tweets have been retrieved so far...')

        if(tweets_retrieved > 8000000):
            logging.warn(f'8 million tweets have been retrieved. Stopping...')
            break

        total_replies[journalist_id] = replies

    current_date = datetime.datetime.now()
    logging.info(f'Fetching replies for journalists completed at {current_date}...')
    return total_replies

def get_replies_for_journalist(journalist_id):
    logging.info(f'Fetching replies for journalist {journalist_id}...')

    client = get_client()
    replies = [] 
    try:
        response = get_raw_replies(client, journalist_id)
    except Exception as e:
        logging.error(f'An error ocurred while fetching replies for journalist {journalist_id}: {e}')
        return replies

    while True:
        try:
            replies = replies + response['data']

            if ('next_token' in response['meta']):
                response = get_raw_replies(client, journalist_id, response['meta']['next_token'])
                continue
            else:
                break
        except tweepy.TweepyException as e:
            logging.error(f'A tweepy error ocurred while fetching replies for journalist {journalist_id}: {e}')
            break 
        except StopIteration as e:
            break
        except Exception as e:
            logging.error(f'An error ocurred while fetching replies for journalist {journalist_id}: {e}')
            break

    logging.info(f'Successfuly fetched {len(replies)} replies for journalist {journalist_id}')
    
    return replies


def get_client():
    client = tweepy.Client(
        bearer_token=credentials.BEARER_TOKEN, 
        consumer_key=credentials.CONSUMER_KEY,
        consumer_secret=credentials.CONSUMER_SECRET,
        access_token=credentials.ACCESS_TOKEN,
        access_token_secret=credentials.ACCESS_SECRET,
        return_type=dict,
        wait_on_rate_limit=True)
    
    return client

def get_raw_replies(client, journalist_id, next_token=None):
    response = client.search_all_tweets(
        query=f'to:{journalist_id}', 
        start_time='2022-10-26T00:00:00Z',
        max_results=500,
        next_token=next_token,
        tweet_fields=['id', 'text', 'attachments', 'author_id', 'conversation_id', 'created_at', 'entities','public_metrics', 'withheld'],
        user_fields=['id', 'name', 'username', 'created_at', 'description', 'entities', 'location', 'pinned_tweet_id', 'profile_image_url', 'protected', 'public_metrics', 'url', 'verified', 'withheld'])

    return response

def save_replies_to_file(replies, tweets_retrieved):
    if len(replies) == 0:
        file_name = str(random.randint(1, 100000)) + '.json'
    else:
        file_name = str(tweets_retrieved) + '.json'
    with open(f'twitter/data/{file_name}', 'w') as f:
        json.dump(replies, f)