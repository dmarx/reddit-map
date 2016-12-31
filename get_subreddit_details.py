import time
import praw
import ConfigParser
import csv
try:
    import ujson as json
except:
    import json

config = ConfigParser.ConfigParser()
config.read('praw_credentials.cfg')

r = praw.Reddit(client_id     = config.get('praw', 'client_id'),
                client_secret = config.get('praw', 'client_secret'),
                user_agent    = config.get('praw', 'user_agent'))

                
                

subreddits = []
with open('active_subreddits_users.csv', 'r') as f:
    reader = csv.reader(f)
    reader.next()
    for line in reader:
        subreddits.append(line[0])

subreddit_details = {}
errors = []
backoff = 2
while len(subreddits)>0:
        #subreddit_name = line[0]
        try:
            backoff = 2
            subreddit_name = subreddits[0]
            subr = r.subreddit(subreddit_name)
            d = {'title':subr.title, 
                 #'description':subr.description, # Title does this well enough. Most descriptions are long and markdown heavy.
                 'subscribers':subr.subscribers}
            subreddit_details[subreddit_name] = d
            print(subreddit_name, subr.subscribers)
            subreddits.remove(subreddit_name)
        except Exception, e:
            print(e)
            errors.append(subreddit_name)
            subreddits.remove(subreddit_name)
            #time.sleep(backoff)
            #backoff*=2

with open('active_subreddit_details.json', 'wb') as outfile:
    json.dump(subreddit_details , outfile)