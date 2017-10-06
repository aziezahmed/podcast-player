import os
import sys
from os.path import expanduser
from sqlobject import *
import feedparser

class PodcastDatabase(SQLObject):
    name = StringCol()
    url = StringCol()

class DataStore():
    def __init__(self):
        
        self.basedir = "~/.podcast"
            
        PodcastDatabase._connection = sqlite.builder()(expanduser(self.basedir + os.sep + 'podcast.sqlite'), debug=False)
        PodcastDatabase.createTable(ifNotExists=True)
        
        podcasts = list(PodcastDatabase.select())
        podcast_urls = []
        
        for podcast in podcasts:
            podcast_urls.append(podcast.url)
        
        self.podcasts = podcast_urls

    def get_podcasts(self):
        return self.podcasts

    def add_podcast(self, podcast_url):
        self.podcasts.append(podcast_url)
        feed = feedparser.parse(podcast_url)
        PodcastDatabase(name=feed.feed.title, url=podcast_url)
