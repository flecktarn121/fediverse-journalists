import constants
import json
from client import TwitterClient


class TweetClient(TwitterClient):

    def __init__(self, tweets_filename: str) -> None:
        super().__init__()
        self.tweets_ids_by_user = self.__load_tweets_ids_(tweets_filename)

    def __load_tweets_ids_(self, tweets_filename: str) -> dict:
        tweets_ids_by_user = {}
        with open(tweets_filename, 'r') as f:
            tweets_ids_by_user = json.load(f)

        return tweets_ids_by_user
    
    def get_raw_posts(self, user_id: str, next_token: str = None) -> dict:
        posts_ids = self.tweets_ids_by_user[user_id]
        #separate the list of ids into chunks of 100
        posts_ids_by_100 = [posts_ids[i:i + 100] for i in range(0, len(posts_ids), 100)]
        posts = []

        for ids in posts_ids_by_100:
            response = self.client.get_tweets(
                ids=ids,
                start_time=constants.START_DATE,
                max_results=constants.MAX_RESULTS,
                next_token=next_token,
                tweet_fields=['id', 'text', 'attachments', 'author_id', 'conversation_id', 'created_at', 'entities','public_metrics', 'withheld'],
                user_fields=['id', 'name', 'username', 'created_at', 'description', 'entities', 'location', 'pinned_tweet_id', 'profile_image_url', 'protected', 'public_metrics', 'url', 'verified', 'withheld'])
            posts.extend(response['data'])

        return response
