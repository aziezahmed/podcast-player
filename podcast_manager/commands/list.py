"""The list command. Used to list the podcast library. """

from json import dumps

from .base import Base

from podcast_manager.datastore import DataStore

class List(Base):

    def run(self):
        dataStore = DataStore()
        podcasts = dataStore.get_podcast_names()
        for podcast in podcasts:
            print(podcast)
