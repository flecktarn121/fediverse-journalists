import constants
from client import TwitterClient

    
class QuoteClient(TwitterClient):

    def get_raw_posts(self,user_id: str, next_token: str=None) -> dict:
        response = self.client.search_all_tweets(
            query=f'twitter.com/{user_id}/ -from:{user_id}', 
            start_time=constants.START_DATE,
            max_results=constants.MAX_RESULTS,
            next_token=next_token,
            tweet_fields=['id', 'text', 'attachments', 'author_id', 'conversation_id', 'created_at', 'entities','public_metrics', 'withheld'],
            user_fields=['id', 'name', 'username', 'created_at', 'description', 'entities', 'location', 'pinned_tweet_id', 'profile_image_url', 'protected', 'public_metrics', 'url', 'verified', 'withheld'])

        return response
