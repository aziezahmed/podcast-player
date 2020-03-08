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

from docopt import docopt
from podcast_player.podcast_player import PodcastPlayer
from . import __version__ as VERSION

def main():

    options = docopt(__doc__, version=VERSION)

    podcast_player = PodcastPlayer()
    
    #print ("Main / options {}".format(options))

    if(options["add"]):
        podcast_player.add_podcast(options["<url>"])

    elif(options["set-player"]):
        podcast_player.set_player(options["<player>"])

    elif(options["delete"]):
        podcast_player.delete_podcast_menu()

    elif(options["-i"]):
        podcast_player.import_opml(options["<opml-file>"])
        
    else:
        podcast_player.main_menu()

