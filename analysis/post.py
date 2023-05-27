import html2text
import datetime
from dateutil.parser import parse


class Post:

    def __init__(self, id, timestamp, handle, user_id, user_bio, uri, text):
        self.id = id
        self.timestamp = timestamp
        self.handle = handle
        self.user_id = user_id
        self.user_bio = user_bio
        self.uri = uri
        self.text = text
        self.tokenized_text = []

    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp,
            'handle': self.handle,
            'user_id': self.user_id,
            'user_bio': self.user_bio,
            'uri': self.uri,
            'text': self.text
        }
    
    @classmethod
    def load_twitter_post(cls, twitter_post):
        
        id = twitter_post['id']
        timestamp = twitter_post['created_at']
        handle = ''
        user_id = twitter_post['author_id']
        user_bio = ''
        uri = f'https://twitter.com/twitter/status/{id}'
        text = html2text.html2text(twitter_post['text'])

        return cls(id, timestamp, handle, user_id, user_bio, uri, text)

    @classmethod
    def load_mastodon_post(cls, mastodon_post):
        
        id = mastodon_post['account']['id']
        timestamp = mastodon_post['created_at']
        handle = mastodon_post['account']['acct']
        user_id = mastodon_post['account']['id']
        user_bio = html2text.html2text(mastodon_post['account']['note'] if 'note' in mastodon_post['account'] else '')
        uri = mastodon_post['uri']
        text = html2text.html2text(mastodon_post['content'])

        return cls(id, timestamp, handle, user_id, user_bio, uri, text)
    
    @classmethod
    def load_from_json(cls, json_post):
            
            id = json_post['id']
            timestamp = parse(json_post['timestamp'])
            handle = json_post['handle']
            user_id = json_post['user_id']
            user_bio = json_post['user_bio']
            uri = json_post['uri']
            text = json_post['text']
    
            return cls(id, timestamp, handle, user_id, user_bio, uri, text)