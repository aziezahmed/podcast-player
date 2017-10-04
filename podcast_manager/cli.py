"""
podcast

Usage:
  podcast list
  podcast add <url>
  podcast -h | --help
  podcast --version

Options:
  -h --help                         Show this screen.
  --version                         Show version.

Examples:
  podcast
  podcast add <url>

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/rdegges/skele-cli
"""

from inspect import getmembers, isclass

from docopt import docopt

from . import __version__ as VERSION
from podcast_manager.datastore import DataStore
from podcast_manager.feed import Feed

def main():

    dataStore = DataStore()

    options = docopt(__doc__, version=VERSION)

    if (options["add"]):
        dataStore.add_podcast(options["<url>"])

    if (options["list"]):
        podcasts = dataStore.get_podcasts()
        for podcast in podcasts:
            fd = Feed(podcast)
            fd.parse()
