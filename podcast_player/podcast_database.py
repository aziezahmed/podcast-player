"""An SQL Object to store information about our podcast library. """

from sqlobject import *
import feedparser

class PodcastDatabase(SQLObject):
    """A database of podcast names and urls."""
    name = StringCol()
    url = StringCol()
