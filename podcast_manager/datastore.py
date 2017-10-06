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

    def get_podcast_urls(self):
        podcasts = list(PodcastDatabase.select())
        podcast_urls = []
        
        for podcast in podcasts:
            podcast_urls.append(podcast.url)
        
        return podcast_urls

    def get_podcast_names(self):
        podcasts = list(PodcastDatabase.select())
        podcast_names = []
        
        for podcast in podcasts:
            podcast_names.append(podcast.name)
        
        return podcast_names

    def add_podcast(self, podcast_url):
        self.podcasts.append(podcast_url)
        feed = feedparser.parse(podcast_url)
        PodcastDatabase(name=feed.feed.title, url=podcast_url)
