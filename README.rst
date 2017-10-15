podcast-player
==============

A command-line podcast player. Stream episodes from your favourite podcasts.
Requires mplayer or mpv.

Getting Started
---------------

Prerequisites
~~~~~~~~~~~~~

-  `Python`_
-  `MPV`_ or `mplayer`_

Installing
~~~~~~~~~~

Podcast Player is on `PyPi`_ so it can be installed with pip.

.. code-block:: bash

    $ pip install podcast-player
	
Setup
~~~~~

To begin we need to add some podcast rss feeds and set the desired audio player (optional)

.. Code-block:: bash

    $ podcast add http://my-podcast-url/feed.rss

The default audio player is mplayer. If desired you can change that.

.. Code-block:: bash

    $ podcast set-player mpv

Usage
~~~~~

Once you have added all the podcasts you want to sbscribe to, then simply run the 'podcast' command to select the podcast and the episode you want to listen to.

    $ podcast
    
