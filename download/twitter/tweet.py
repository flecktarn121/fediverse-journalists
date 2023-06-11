import constants
from client import TwitterClient


class TweetClient(TwitterClient):

    def get_raw_posts(self,user_id: str, next_token: str|None=None) -> dict:
        response = self.client.search_all_tweets(
            query=f'from:{user_id} -is:retweet', 
            start_time=constants.START_DATE,
            end_time=constants.END_DATE,
            max_results=constants.MAX_RESULTS,
            next_token=next_token,
            tweet_fields=['id', 'text', 'attachments', 'author_id', 'conversation_id', 'created_at', 'entities','public_metrics', 'withheld'],
            expansions=['author_id'],
            user_fields=['id', 'name', 'username', 'created_at', 'description', 'entities', 'location', 'pinned_tweet_id', 'profile_image_url', 'protected', 'public_metrics', 'url', 'verified', 'withheld'])

        return response
