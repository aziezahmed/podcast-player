"""
podcast

Usage:
  podcast
  podcast add <url>
  podcast delete
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

import feedparser
import listparser

from PyInquirer import  prompt
from pprint import pprint 
from . import __version__ as VERSION
from . import UserSettings

class PodcastDatabase(SQLObject):
    """A database of podcast names and urls."""    
    name = StringCol()
    url = StringCol()

def setup():
    """
    Inital Setup:
    Create the database and make a connection to it
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

def add_podcast(url):
    """
    Add a podcast

    Parameters
    ----------
    url : string
        The URL of the podcast to subscribe to.
    """    
    # Look to see if the podcast is already in the directory
    results = list(PodcastDatabase.select(PodcastDatabase.q.url == url))

    # If it is not then we can add it
    if len(results) == 0:    
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

def handle_choice(answers, key):
    """
    Handle user input
    """
    # if there is no input then the user probably ctrl+c'ed out
    if len(answers) == 0:
        sys.exit(0)
    
    # handle the back and quit
    inp = answers[key]
    if inp == "Back":
        podcast_menu()
    elif inp == "Quit":
        sys.exit(0)

def delete_podcast_menu():
    """
    The delete menu
    Here we list all the podcasts that the user is subscribed to
    and allow the user to choose which one they want to delete
    """
    podcasts = PodcastDatabase.select()
    
    if podcasts.count() == 0:
        print("There are no podcasts to delete!\n")
        sys.exit(0)
    
    podcast_names = []
    for podcast in podcasts:
        podcast_names.append({'name': podcast.name})

    questions = [
        {
            'type': 'checkbox',
            'name': 'podcasts',
            'message': 'What episode do you want to listen to?',
            'choices': podcast_names
        }
    ]

    answers = prompt(questions)
    handle_choice(answers, 'podcasts')

    podcasts = answers["podcasts"]

    for podcast in podcasts:
        index = list(PodcastDatabase.select(PodcastDatabase.q.name == podcast))[0].id
        PodcastDatabase.delete(index)

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
    titles = []

    for index, entry in enumerate(feed.entries):
        titles.append(entry['title'])
    
    titles.append("Back")
    titles.append("Quit")

    questions = [
        {
            'type': 'list',
            'name': 'episode',
            'message': 'What episode do you want to listen to?',
            'choices': titles
        }
    ]

    answers = prompt(questions)
    handle_choice(answers, 'episode')

    choice = titles.index(answers["episode"])
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
    podcasts = PodcastDatabase.select()
    
    if podcasts.count() == 0:
        print("There are no podcast feeds found.")
        print("To add a podcast use the 'add' parameter:\n")
        print("podcast add http://www.mypodcast.com/feed.rss\n")
        sys.exit(0)
    
    podcast_names = []

    for index, podcast in enumerate(podcasts):
        podcast_names.append(podcast.name)

    podcast_names.append("Quit")

    questions = [
        {
            'type': 'list',
            'name': 'podcast',
            'message': 'What podcast do you want to listen to?',
            'choices': podcast_names
        }
    ]

    answers = prompt(questions)
    handle_choice(answers,'podcast')

    podcast = PodcastDatabase.select(PodcastDatabase.q.name == answers["podcast"])
    episode_menu(list(podcast)[0])

def main():
    """
    The main function. We will establish a connnection to the database and
    process the user's command.
    """
    setup()

    # Run the docopt
    options = docopt(__doc__, version=VERSION)

    if(options["add"]):
        add_podcast(options["<url>"])

    elif(options["set-player"]):
        set_player(options["<player>"])

    elif(options["delete"]):
        delete_podcast_menu()

    elif(options["-i"]):
        import_opml(options["<opml-file>"])
        
    else:
        podcast_menu()
