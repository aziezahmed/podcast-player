Podcast Player
==============

*A command line application for displaying news headlines, written in Python.*

Getting Started
---------------

Prerequisites
~~~~~~~~~~~~~

-  `Python`_
-  mpv or mplayer

Installing
~~~~~~~~~~

Podcast Player is on PyPi so it can be installed with pip.

.. code-block:: bash

    $ pip install podcast-player

Setup
~~~~~

To begin we need to add some podcast rss feeds and set the desired audio player (optional)

.. Code-block:: bash

    $ podcast add URL

The default audio player is mplayer. If desired you can change that.

.. Code-block:: bash

    $ podcast set-player mpv

Usage
~~~~~

Once you have added all the podcasts you want to subscribe to, then simply run the 'podcast' command to select the podcast and the episode you want to listen to.

.. code-block:: bash

    $ podcast


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
