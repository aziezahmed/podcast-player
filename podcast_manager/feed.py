import feedparser
import hashlib

class Feed():
    def __init__(self, podcast_url):
        self.url = podcast_url

    def parse(self):
        feed = feedparser.parse(self.url)
        feed.entries.reverse()
        for entry in feed.entries:
            print(entry['title'])
            print(entry["link"])
