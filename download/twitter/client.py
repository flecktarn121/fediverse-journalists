import tweepy
import logging
import credentials
import json
import datetime
import constants


class TwitterClient:

    def __init__(self) -> None:
        self.file_counter: int = 0
        self.posts_retrieved = 0
        self.client: tweepy.Client = self.__get_client()
        
    def retrieve_posts(self, ids: list[str]) -> None:
        current_date = datetime.datetime.now()
        logging.info(f'Fetching posts started at {current_date}...')

        for id in ids:
            posts = self.get_posts_for_id(id)
            self.posts_retrieved += len(posts)
            self.__save_posts_to_file(posts)
            logging.info(f'A total of {self.posts_retrieved} tweets have been retrieved so far...')

            if(self.posts_retrieved > constants.MAX_POSTS):
                logging.warn(f'{constants.MAX_POSTS} tweets have been retrieved. Stopping...')
                break

        current_date = datetime.datetime.now()
        logging.info(f'Fetching posts for user completed at {current_date}...')
    
    def get_posts_for_id(self, id: str) -> list[dict]:
        logging.info(f'Fetching replies for user {id}...')

        posts = [] 
        try:
            response = self.get_raw_posts(id)
        except Exception as e:
            logging.error(f'An error ocurred while fetching posts for user {id}: {e}')
            return posts

        while True:
            try:
                posts = posts + self.__process_response(response)

                if ('next_token' in response['meta']):
                    response = self.get_raw_posts(id, response['meta']['next_token'])
                    continue
                else:
                    break
            except tweepy.TweepyException as e:
                logging.error(f'A tweepy error ocurred while fetching posts for user {id}: {e}')
                break 
            except StopIteration as e:
                break
            except Exception as e:
                logging.error(f'An error ocurred while fetching posts for user {id}: {e}')
                break

        logging.info(f'Successfuly fetched {len(posts)} posts for user {id}')
        
        return posts

    def get_raw_posts(self,user_id: str, next_token: str=None) -> dict:
        response = self.client.search_all_tweets(
            query=f'to:{user_id}', 
            start_time=constants.START_DATE,
            max_results=constants.MAX_RESULTS,
            next_token=next_token,
            tweet_fields=['id', 'text', 'attachments', 'author_id', 'conversation_id', 'created_at', 'entities','public_metrics', 'withheld'],
            user_fields=['id', 'name', 'username', 'created_at', 'description', 'entities', 'location', 'pinned_tweet_id', 'profile_image_url', 'protected', 'public_metrics', 'url', 'verified', 'withheld'])

        return response

    def __get_client(self) -> tweepy.Client:
        client = tweepy.Client(
            bearer_token=credentials.BEARER_TOKEN, 
            consumer_key=credentials.CONSUMER_KEY,
            consumer_secret=credentials.CONSUMER_SECRET,
            access_token=credentials.ACCESS_TOKEN,
            access_token_secret=credentials.ACCESS_SECRET,
            return_type=dict,
            wait_on_rate_limit=True)
        
        return client

    def __save_posts_to_file(self, posts: list) -> None:
        filename = f'{constants.FILE_PREFIX}{self.file_counter}.json'
        with open(f'{constants.DESTINATION_DIRERCTORY}{filename}', 'w') as f:
            json.dump(posts, f)
        
        self.file_counter += 1
    
    def __process_response(self, response: dict) -> list[dict]:
        posts = []
        if ('data' in response):
            posts = response['data']
        
        if ('includes' in response and 'users' in response['includes']):
            users = response['includes']['users']
            for post in posts:
                post['author'] = next((user for user in users if user['id'] == post['author_id']), '')
        
        return posts
    