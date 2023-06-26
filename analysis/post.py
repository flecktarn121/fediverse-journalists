from __future__ import annotations
import html2text
from dateutil.parser import parse


class Post:

    def __init__(self, id, timestamp, handle, user_id, user_bio, uri, text) -> None:
        self.id = id
        self.timestamp = timestamp
        self.handle = handle
        self.user_id = user_id
        self.user_bio = user_bio
        self.uri = uri
        self.text = text
        self.verbatim_text = text
        self.tokenized_text = []
        self.entities = []
        self.urls = set()
        self.mentions = set()
        self.hashtags = set()

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'timestamp': str(self.timestamp),
            'handle': self.handle,
            'user_id': self.user_id,
            'user_bio': self.user_bio,
            'uri': self.uri,
            'text': self.text,
            'verbatim_text': self.verbatim_text,
            'entities': list(self.entities),
            'urls': list(self.urls),
            'mentions': list(self.mentions),
            'hashtags': list(self.hashtags)
        }

    @classmethod
    def __get_html2text(cls) -> html2text.HTML2Text:
        processor = html2text.HTML2Text()
        processor.ignore_links = True # prevent noise in hastags and mentions links
        processor.body_width = 0 # No random line breaks

        return processor
    
    @classmethod
    def load_twitter_post(cls, twitter_post: dict) -> Post:
        processor = cls.__get_html2text()
        
        id = twitter_post['id']
        timestamp = twitter_post['created_at']
        handle = ''
        user_id = twitter_post['author_id']
        user_bio = ''
        uri = f'https://twitter.com/twitter/status/{id}'
        text = processor.handle(twitter_post['text']).strip()

        return cls(id, timestamp, handle, user_id, user_bio, uri, text)

    @classmethod
    def load_mastodon_post(cls, mastodon_post: dict) -> Post:
        processor = cls.__get_html2text()
        
        id = mastodon_post['account']['id']
        timestamp = mastodon_post['created_at']
        handle = mastodon_post['account']['acct']
        user_id = mastodon_post['account']['id']
        user_bio = processor.handle(mastodon_post['account']['note'] if 'note' in mastodon_post['account'] else '').strip()
        uri = mastodon_post['uri']
        text = processor.handle(mastodon_post['content']).strip()

        return cls(id, timestamp, handle, user_id, user_bio, uri, text)
    
    @classmethod
    def load_from_json(cls, json_post: dict) -> Post:
            
            id = json_post['id']
            timestamp = parse(json_post['timestamp'])
            handle = json_post['handle']
            user_id = json_post['user_id']
            user_bio = json_post['user_bio']
            uri = json_post['uri']
            text = json_post['text']
            entities = json_post['entities']
            verbatim_text = json_post['verbatim_text']
            urls = json_post['urls']
            mentions = json_post['mentions']
            hashtags = json_post['hashtags']

            post = cls(id, timestamp, handle, user_id, user_bio, uri, text)
            post.verbatim_text = verbatim_text
            post.entities = entities
            post.urls = set(urls)
            post.mentions = set(mentions)
            post.hashtags = set(hashtags)

            return post