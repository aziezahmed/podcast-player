"""
podcast

Usage:
  podcast list
  podcast hello
  podcast add <url>
  podcast -h | --help
  podcast --version

Options:
  -h --help                         Show this screen.
  --version                         Show version.

Examples:
  podcast list
  podcast add <url>

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/aziezahmed/podcast-manager
"""

from inspect import getmembers, isclass

from docopt import docopt

from . import __version__ as VERSION
from podcast_manager.datastore import DataStore
from podcast_manager.feed import Feed


def main():
    import podcast_manager.commands
    
    dataStore = DataStore()
    
    import podcast_manager.commands
    
    options = docopt(__doc__, version=VERSION)

    for (k, v) in options.items(): 
        if hasattr(podcast_manager.commands, k) and v:
            module = getattr(podcast_manager.commands, k)
            podcast_manager.commands = getmembers(module, isclass)
            command = [command[1] for command in podcast_manager.commands if command[0] != 'Base'][0]
            command = command(options)
            command.run()

    if (options["add"]):
        dataStore.add_podcast(options["<url>"])

    if (options["list"]):
        podcasts = dataStore.get_podcasts()
        for podcast in podcasts:
            fd = Feed(podcast)
            fd.parse()
