"""
podcast

Usage:
  podcast
  podcast list
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

from docopt import docopt

from . import __version__ as VERSION

def main():

    import podcast_player.commands

    options = docopt(__doc__, version=VERSION)

    if(options["list"]):
        list = podcast_player.commands.List(options)
        list.run()
    elif(options["add"]):
        add = podcast_player.commands.Add(options)
        add.run()
    else:
        parse = podcast_player.commands.Parse(options)
        parse.run()
