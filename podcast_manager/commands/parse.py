
from json import dumps

from .base import Base

from podcast_manager.datastore import DataStore

import feedparser

class Parse(Base):

    def run(self):
        dataStore = DataStore()
        podcasts = dataStore.get_podcasts()
        data = []
        for podcast in podcasts:
            feed = feedparser.parse(podcast)
            data.append(feed)
        for index, feed in enumerate(data):
            print(str(index+1) + " - " + feed.feed.title)
        choice = input('Which feed: ')
        feed = data[int(choice)-1]
        feed.entries.reverse()
        for index, entry in enumerate(feed.entries):
            print(str(index+1) + " - " + entry['title'])
        choice = input('Which episode: ')
        print(feed.entries[int(choice)-1]["link"])
