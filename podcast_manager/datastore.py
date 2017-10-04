import os
import sys
from os.path import expanduser

class DataStore():
    def __init__(self):
        self.basedir = "~/.podcast"
        if not os.path.exists(expanduser(self.basedir)):
            print("Creating base dir %s"%self.basedir)
            os.makedirs(expanduser(self.basedir))
        subscriptions = expanduser(self.basedir) + os.sep + 'subscriptions'
        if not os.path.exists(subscriptions):
            print("Creating empty subscriptions file %s"%subscriptions)
            open(subscriptions,'a').write("# Add your RSS/ATOM subscriptions here.\n\n")
        subscribed_feeds = []
        with open(subscriptions, 'r') as f:
            for line in f:
                feed = line.strip()
                if feed.startswith("#") or len(feed) == 0:
                    continue
                subscribed_feeds.append(feed)
        self.podcasts = subscribed_feeds

    def get_podcasts(self):
        return self.podcasts

    def add_podcast(self, podcast_url):
        self.podcasts.append(podcast_url)

        subscriptions = expanduser(self.basedir) + os.sep + 'subscriptions'
        with open(subscriptions, 'a') as f:
            f.write(podcast_url + "\n")
