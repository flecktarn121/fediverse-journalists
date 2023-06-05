import csv
import logging
import replies


def load_journalists_from_file(file_path):
    journalists_ids = []
    
    with open(file_path, 'r') as f:
        for line in csv.reader(f):
            journalists_ids.append(line[3])
    
    return journalists_ids

def save_replies_to_file(replies):
    with open('data/replies.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['journalist_id', 'reply_id', 'reply_text'])
        for journalist_id, replies in replies.items():
            for reply in replies:
                writer.writerow([journalist_id, reply.id, reply.text])

def main():
    logging.basicConfig(
        filename='info.log',
        level=logging.INFO, 
        encoding='utf-8')
    
    journalists_ids = load_journalists_from_file('twitter/data/journalists.csv')
    retrieved_replies = replies.get_replies(journalists_ids)
    #save_replies_to_file(retrieved_replies)

if __name__ == '__main__':
    main()