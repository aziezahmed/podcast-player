"""The add command. Used to add a podcast to the podcast library. """

from json import dumps

from .base import Base

from podcast_player.datastore import DataStore

class Add(Base):

    def run(self):
        dataStore = DataStore()
        dataStore.add_podcast(self.options["<url>"])
