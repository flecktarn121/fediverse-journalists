import logging
import csv
import replies
from multiprocessing import Pool, cpu_count

def read_journalists_ids():
    journalists_by_domain = {}
    with open('mastodon/data/journalists.csv', 'r') as f:
        try:
            process_row(journalists_by_domain, f)
        except Exception as e:
            pass

    return journalists_by_domain

def process_row(journalists_by_domain, f):
    reader = csv.reader(f)
    for row in reader:
        user = row[2]
        domain = get_domain_from_username(user)
        if domain in journalists_by_domain:
            journalists_by_domain[domain].append(row[2])
        else:
            journalists_by_domain[domain] = [row[2]]

def get_domain_from_username(username):
    return username.split('@')[-1]

def main():
    journalists_by_domain = read_journalists_ids()
    # get the values of the dictionary
    journalists_ids = journalists_by_domain.values()
    pool = Pool(cpu_count())
    pool.map(replies.get_replies, journalists_ids)



if __name__ == '__main__':
    main()