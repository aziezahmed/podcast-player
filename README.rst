Podcast Player
==============

|PyPI version|

*A command line podcast player, written in Python.*

Getting Started
---------------

Prerequisites
~~~~~~~~~~~~~

-  `Python`_
-  mpv or mplayer

Installing
~~~~~~~~~~

Podcast Player is on PyPI so it can be installed with pip.

.. code-block:: bash

    $ pip install podcast-player


Setup
~~~~~

To begin we need to add some podcast rss feeds. This is done one by one with the following command.

.. code-block:: bash

    $ podcast add URL

If you have an OPML file with podcast subscriptions that you would like to import then you can do so with the opml argument.

.. code-block:: bash

    $ podcast opml OPMLFILE

The default audio player is mpv in no-video mode. If desired you can change that.

.. code-block:: bash

    $ podcast set-player mplayer

Usage
~~~~~

Once you have added all the podcasts you want to subscribe to, then simply run the 'podcast' command to select the podcast and the episode you want to listen to.

.. code-block:: bash

    $ podcast

For more details run with the help option

.. code-block:: bash
		
    $ podcast --help

    podcast

    Usage:
      podcast
      podcast add <url>
      podcast opml <opml>
      podcast set-player <player>
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


Built With
----------

-  `skele-cli`_

Authors
-------

-  `Aziez Ahmed Chawdhary`_

License
-------

This project is licensed under the MIT License

.. _Python: https://www.python.org
.. _PyPi: https://pypi.python.org/pypi
.. _skele-cli: https://github.com/rdegges/skele-cli
.. _Aziez Ahmed Chawdhary: https://github.com/aziezahmed
.. |PyPI version| image:: https://img.shields.io/pypi/v/podcast-player.svg
   :target: https://pypi.python.org/pypi/podcast-player
