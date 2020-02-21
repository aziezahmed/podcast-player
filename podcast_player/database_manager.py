from podcast_player.database import PodcastDatabase
from podcast_player.user_settings import UserSettings
import sqlobject
from sqlobject.sqlite import builder
import os
from os.path import expanduser


class PodcastDatabaseManager(object):
    """
    Access to database layer of podcasts.
    """

    def __init__(self, debug_=False):
        """
        Create the database and make a connection to it.
        """
        basedir = "~/.podcast"
        path = basedir + os.sep + 'podcast.sqlite'

        # If the ~/.podcast directory does not exist, let's create it.
        if not os.path.exists(expanduser(basedir)):
            print("Creating base dir %s"%basedir)
            os.makedirs(expanduser(basedir))

        # Make a connection to the DB. Create it if it does not exist
        PodcastDatabase._connection = builder()(expanduser(path), debug=debug_)
        PodcastDatabase.createTable(ifNotExists=True)
        self.debug_ = debug_
    
    def get_all_subscribed_podcasts(self):
        """
        Return all the podcasts found in database.
        """
        podcasts = PodcastDatabase.select()
        if self.debug_:
            print(podcasts)
        return podcasts
    
    def get_matching_podcast(self, podcast_name):
        """
        Return matching PodcastDatabase podcast for a given podcast name.
        NB: assumption is that podcast_name will always be found as used 
        in the context of the podcast player.

        Parameters
        ----------
        podcast_name : string to compare against names of the podcast stored in database.
        """
        return list(PodcastDatabase.select(PodcastDatabase.q.name == podcast_name))[0]

    def add_podcast(self, podcast):
        """
        Add a podcast

        Parameters
        ----------
        podcast : Podcast to add.
        """    
        if not self.is_podcast_already_added(podcast.url):            
            PodcastDatabase(name=podcast.title, url=podcast.url)
            if self.debug_:
                print("Podcast <{0}> registered".format(podcast))
        else:
            if self.debug_:
                print ("Podcast <{0}> already registered".format(podcast))
    
    def is_podcast_already_added(self, podcast_url):
        """
        Return True if a podcast with the same url than podcast_url is registered in database, False otherwise.

        Parameters
        ----------
        podcast_url : string
            The URL of the podcast to check.
        """
        return PodcastDatabase.select(PodcastDatabase.q.url == podcast_url).count() > 0

    def delete(self, podcast_names):
        """
        Remove a list of podcast names from the database of subscribed podcasts.
        """
        if self.debug_:
            print("Podcasts to delete: [{}]".format(podcast_names))
        for podcast_name in podcast_names:
            print("Deleting podcast [{}]".format(podcast_name))
            id_ = list(PodcastDatabase.select(PodcastDatabase.q.name == podcast_name))[0].id
            PodcastDatabase.delete(id_)
