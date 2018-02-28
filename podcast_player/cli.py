"""
podcast

Usage:
  podcast
  podcast add <url>
  podcast set-player <player>
  podcast -i <opml-file>
  podcast -h | --help
  podcast --version

Options:
  -h --help                         Show this screen.
  --version                         Show version.

Examples:
  podcast 
  podcast set-player mpv
  podcast set-player mplayer
  podcast add https://my-podcast-url.com/feed.rss

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/aziezahmed/podcast-player
"""
import os
import sys
import feedparser

from docopt import docopt
from os.path import expanduser
from sqlobject import *
from tabulate import tabulate

import feedparser
import listparser

from . import __version__ as VERSION
from . import UserSettings

class PodcastDatabase(SQLObject):
    """A database of podcast names and urls."""
    name = StringCol()
    url = StringCol()

def list_podcasts():
    """
    List the names of all the subscribed podcasts.
    """

    podcasts = list(PodcastDatabase.select())
    for podcast in podcasts:
        print(podcast.name)
        print(podcast.url)
        print("-"*len(podcast.url))

def add_podcast( url):
    """
    Add a podcast

    Parameters
    ----------
    url : string
        The URL of the podcast to subscribe to.
    """

    podcast_check_list = list(PodcastDatabase.select(PodcastDatabase.q.url == url))

    if len(podcast_check_list) == 0:    
        feed = feedparser.parse(url).feed
        name = url
        if hasattr(feed, "title"):
            name = feed.title
            new_feed = PodcastDatabase(name=name, url=url)
            
def import_opml(opml_file):
    """
    Import feeds from an opml file
    
    Parameters
    ----------
    opml_file : string
        The relative path to the opml file that we want to import. 

    """
    print("importing " + opml_file)
    
    new_feeds = listparser.parse(opml_file)
    for feed in new_feeds.feeds:
        print(feed.url)
        add_podcast(feed.url)
    
def delete_podcast_menu():
    """
    The delete menu
    Here we list all the podcasts that the user is subscribed to
    and allow the user to choose which one they want to delete
    """

    os.system('clear')
    podcasts = PodcastDatabase.select()
    
    if podcasts.count() == 0:
        print("There are no podcasts to delete!\n")
        sys.exit(0)
    
    for podcast in podcasts:
        print("[ " + str(podcast.id) + " ] - " + podcast.name)
    print("\n[ q ] - Quit")
    print("\nEnter the id of the podcast you wish to delete.")
    choice = handle_choice()

    podcast_check_list = list(PodcastDatabase.select(PodcastDatabase.q.id == choice))
    
    if len(podcast_check_list) == 0:
        delete_podcast_menu()
    else:
        PodcastDatabase.delete(choice) 

def handle_choice():
    """
    Save the preferred media player in the user settings
    """

    choice = input(">>  ")
    choice = choice.lower()
    if choice == "q":
        sys.exit(0)
    elif choice == "b":
        podcast_menu()
    elif choice == "":
        return handle_choice()
    elif not choice.isdigit():
        return handle_choice()
    else:
        return int(choice)

def set_player(player):
    """
    Save the preferred media player in the user settings

    Parameters
    ----------
    player : string
        The player that we pass the media url to when we play a podcast.
    """

    user_settings = UserSettings()
    user_settings.set_media_player(player)

def play_podcast(url):
    """
    Play the podcast using the user's preferred player
    """

    user_settings = UserSettings()
    player = user_settings.get_media_player()
    os.system('clear')
    os.system(player + " "+ url)

def get_episode_media_url(podcast_entry):
    """
    Extract the media URL from the podcast entry

    Parameters
    ----------
    podcast_entry : object
        The entry object from the feed.
    """

    links = podcast_entry["links"]
    for link in links:
        if "audio" in link["type"]:
            return link["href"]

def episode_menu(podcast):
    """
    The episode menu
    Here we list all the episodes of the selected podcast
    and allow the user to choose which one they want to listen to

    Parameters
    ----------
    podcast : PodcastDatabase
        The podcast entry from the database
    """

    feed = feedparser.parse(podcast.url)

    os.system('clear')

    feed.entries.reverse()

    table = []
    headers = ["choice","title"]
    
    for index, entry in enumerate(feed.entries):
        table.append([str(index+1), entry['title']])
           
    print(tabulate(table,headers,tablefmt="simple"))
        
    print("\nEnter the number of the episode you wish to listen to.")
    print("Enter b to go back or q to quit.")

    choice = handle_choice()
    choice = choice - 1
    
    if(0 <= choice < len(feed.entries)):
        entry = feed.entries[choice]
        url = get_episode_media_url(entry)
        if type(url) is str:
            play_podcast(url)

    episode_menu(podcast)   
 
def podcast_menu():
    """
    The main menu
    Here we list all the podcasts that the user is subscribed to
    and allow the user to choose which one they want to see the episodes of
    At that point we move to the episode menu
    """

    os.system('clear')
    podcasts = PodcastDatabase.select()
    
    if podcasts.count() == 0:
        print("There are no podcast feeds found.")
        print("To add a podcast use the 'add' parameter:\n")
        print("podcast add http://www.mypodcast.com/feed.rss\n")
        sys.exit(0)
    
    podcast_array = []

    table = []
    headers = ["choice","title"]

    for index, podcast in enumerate(podcasts):
        podcast_array.append(podcast)
        table.append([str(index+1), podcast.name])

    print(tabulate(table,headers,tablefmt="simple"))
        
    print("\nEnter the number of the podcast you wish to listen to.")
    print("Enter q to quit.")
    choice = handle_choice()
    choice = choice - 1

    if(0 <= choice < len(podcast_array)):
        episode_menu(podcast_array[choice])  
    else:
        podcast_menu()


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

    if(options["add"]):
        add_podcast(options["<url>"])

    elif(options["set-player"]):
        set_player(options["<player>"])

    elif(options["-i"]):
        import_opml(options["<opml-file>"])
        
    else:
        podcast_menu()
