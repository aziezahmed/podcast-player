import feedparser
import listparser
import time
from datetime import datetime
from podcast_player.podcast import Podcast, PodcastEntry

class PodcastParser(object):
    """
    Parser to extract Podcast objects from a feed.
    """
    def __init__(self, debug_=False):
        self.debug_ = debug_
        if self.debug_:
            print ("Podcast Parser")
    
    def create_podcast_from(self, podcast_url):
        """
        Create a Podcast object from the url of a podcast to parse.

        Parameters
        ----------
        podcast_url : string
            The url of the podcast to parse.
        """
        feed = feedparser.parse(podcast_url).feed
        if hasattr(feed, "title"):
            return Podcast(url=podcast_url, title=feed.title)
    
    def generate_feeds_from(self, opml_file):
        """
        Yield each podcast parsed from an OPML file.

        Parameters
        ----------
        opml_file : string
        """
        for feed in listparser.parse(opml_file).feeds:
            podcast = Podcast(url=feed.url, title=feed.title if hasattr(feed, "title") else "")
            if self.debug_:
                print ("Handling podcast [{}]".format(podcast))
            yield podcast

    def generate_feed_entries_from(self, podcast_url, debug_=False):
        """
        Yield each podcast entry parsed from the url of a podcast to parse.

        Parameters
        ----------
        podcast_url : string
            The url of the podcast to parse.
        """
        for feed_entry in feedparser.parse(podcast_url).entries:
            published_date = datetime.fromtimestamp(time.mktime(feed_entry.published_parsed))
            podcast_entry = PodcastEntry(feed_entry.title, published_date, self._extract_episode_media_url(feed_entry), debug_=debug_)
            if self.debug_:
                print ("Handling podcast entry [{}]".format(podcast_entry))
            yield podcast_entry
    
    def _extract_episode_media_url(self, feed_entry):
        """
        Extract the url to be played for a given entry of a podcast.

        Parameters
        ----------
        feed_entry : feedparser entry
        """
        links = feed_entry["links"]
        for link in links:
            if "audio" in link["type"]:
                return link["href"]
