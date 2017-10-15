"""
podcast

Usage:
  podcast
  podcast list
  podcast add <url>
  podcast set-player <player>
  podcast -h | --help
  podcast --version

Options:
  -h --help                         Show this screen.
  --version                         Show version.

Examples:
  podcast
  podcast list
  podcast set-player mpv
  podcast set-player mplayer
  podcast add https://my-podcast-url.com/feed.rss

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/aziezahmed/podcast-manager
"""
import os
import sys
import feedparser

from docopt import docopt
from os.path import expanduser
from sqlobject import *

from . import __version__ as VERSION
from . import PodcastDatabase
from . import UserSettings

def list_podcasts():
    """
    List the names of all the subscribed podcasts.
    """
    podcasts = PodcastDatabase.get_podcast_names(PodcastDatabase)
    os.system('clear')
    for podcast in podcasts:
        print(podcast)

def add_podcast(url):
    """
    List the names of all the subscribed podcasts.

    Parameters
    ----------
    url : string
        The URL of the podcast to subscribe to.
    """
    PodcastDatabase.add_podcast(PodcastDatabase, url)

def set_player(player):
    user_settings = UserSettings()
    user_settings.set_media_player(player)

def play_podcast(url):
    user_settings = UserSettings()
    player = user_settings.get_media_player()

    os.system('clear')
    os.system(player + " "+ url)
    

def episode_menu(podcast_choice):
    podcast_urls = PodcastDatabase.get_podcast_urls(PodcastDatabase)
    feed = feedparser.parse(podcast_urls[int(podcast_choice)-1])
    feed.entries.reverse()
    
    choice = ""
    while choice != "b":
        os.system('clear')
        for index, entry in enumerate(feed.entries):
            print(str(index+1) + " - " + entry['title'])
        print("b - Back")
        print("q - Quit")
        choice = input(">>  ")
        if choice.lower() == "q":
            sys.exit(0)
        elif choice.lower() != "b":
            url = feed.entries[int(choice)-1]["link"]
            play_podcast(url)
    podcast_menu()
    

def podcast_menu():
    podcast_names = PodcastDatabase.get_podcast_names(PodcastDatabase)
    os.system('clear')
    for index, name in enumerate(podcast_names):
        print(str(index+1) + " - " + name)
    print("q - Quit")
    choice = input(">>  ")
    if choice.lower() == "q":
        sys.exit(0)
    else:
        episode_menu(choice)


def main():
    """
    The main function. We will establish a connnection to the database and
    process the user's command.
    """

    basedir = "~/.podcast"
    path = basedir + os.sep + 'podcast.sqlite'

    # If the ~/.podcast directory does not exist, let's create it.
    if not os.path.exists(expanduser(basedir)):
        print("Creating base dir %s"%basedir)
        os.makedirs(expanduser(basedir))

    # Make a connection to the DB. Create it if it does not exist
    PodcastDatabase._connection = sqlite.builder()(expanduser(path), debug=False)
    PodcastDatabase.createTable(ifNotExists=True)

    # Run the docopt
    options = docopt(__doc__, version=VERSION)

    if(options["list"]):
        list_podcasts()

    elif(options["add"]):
        add_podcast(options["<url>"])

    elif(options["set-player"]):
        set_player(options["<player>"])

    else:
        podcast_menu()
