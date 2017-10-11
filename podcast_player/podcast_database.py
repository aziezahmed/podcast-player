"""An SQL Object to store information about our podcast library. """

from sqlobject import *
import feedparser

class PodcastDatabase(SQLObject):
    """A database of podcast names and urls."""
    name = StringCol()
    url = StringCol()

    def get_podcast_urls(self):
        """
        Get a string array of all the podcast URLs.

        Returns
        -------
        string_array
            A string array of all the podcast urls
        """
        podcasts = list(self.select())
        podcast_urls = []

        for podcast in podcasts:
            podcast_urls.append(podcast.url)

        return podcast_urls

    def get_podcast_names(self):
        """
        Get all the podcast names from the database.

        Returns
        -------
        string_array
            A string array of all the podcast names
        """
        podcasts = list(self.select())
        podcast_names = []

        for podcast in podcasts:
            podcast_names.append(podcast.name)

        return podcast_names

    def add_podcast(self, podcast_url):
        """
        Add a podcast to the databaseGet a string array of all the podcast URLs.

        Parameters
        ----------
        podcast_url : string
            The URL that you want to add to the database. The name is retreived
            from the feed title.
        """
        feed = feedparser.parse(podcast_url)
        name=feed.feed.title
        url=podcast_url

        check_db = self.select (self.q.name == name).count()
        if check_db == 0:
            PodcastDatabase(name=name,url=url)
