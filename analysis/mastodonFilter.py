import os
import json
import csv

class MatoFilter:

    def __init__(self):
        self.instances = set()
        self.load_instances_blacklist('blacklist.csv')
    
    def load_instances_blacklist(self, filename):
        with open(filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.instances.add(row['instance'])
        print(self.instances)

    def load_toots(self, directory):
        for filename in os.listdir(directory):
            if filename.endswith(".json"):
                print(f'Loading {filename}...')
                posts = json.load(open(os.path.join(directory, filename), 'r'))
                posts = self.process_posts(posts)
                with open(os.path.join(directory, filename), 'w') as outfile:
                    json.dump(posts, outfile, indent=4)
        
    def process_posts(self, posts):
        posts = self.remove_no_index_accounts(posts)
        posts = self.remove_no_bot_account(posts)
        posts = self.remove_bots(posts)
        posts = self.remove_blacklisted_instances(posts)

        return posts
    
    def remove_blacklisted_instances(self, posts):
        return [post for post in posts if not self.__is_instance_blacklisted(post)]
    
    def __is_instance_blacklisted(self, post):
        for instance in self.instances:
            if instance in post['account']['url']:
                return True
        
        return False
    
    def get_instances(self, posts):
        for post in posts:
            instance = post['account']['url'].split('@')[0]
            self.instances.add(instance)

    def remove_no_index_accounts(self, posts):
        return [post for post in posts if not self.__has_no_index_flag(post)]
    
    def __has_no_index_flag(self, post):
        return post['account']['noindex'] if 'noindex' in post['account'] else False
    
    def remove_bots(self, posts):
        return [post for post in posts if not post['account']['bot']]
    
    def remove_no_bot_account(self, posts):
        return [post for post in posts if not self.has_no_bot_tag(post)]
    
    def has_no_bot_tag(self, post):
        bio = post['account']['note']
        fields_values = [str(field['value']) for field in post['account']['fields']]

        no_bot = False
        no_bot |= '#nobot' in bio.lower() or any('#nobot' in field.lower() for field in fields_values)
        no_bot |= '#noindex' in bio.lower() or any('#noindex' in field.lower() for field in fields_values)
        no_bot |= '#noarchive' in bio.lower() or any('#noarchive' in field.lower() for field in fields_values)
        return no_bot

if __name__ == "__main__":
    mato = MatoFilter()
    mato.load_toots('data/split/mastodon')

        
