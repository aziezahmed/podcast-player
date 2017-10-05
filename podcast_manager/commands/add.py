

from json import dumps

from .base import Base

from podcast_manager.datastore import DataStore

class Add(Base):

    def run(self):
        dataStore = DataStore()
        dataStore.add_podcast(self.options["<url>"])
