"""An Object to store and retrive user settings"""

import os, configparser

class UserSettings(object):
    def __init__(self):
        """
        To initialise we create a config parser object with the default 
        player and save it to a file if it does not exist
        """
        self.basedir = "~/.podcast"

        self.user_config_dir = os.path.expanduser(self.basedir);
        self.user_config_path = self.user_config_dir + "/podcast-player.ini"

        self.config = configparser.ConfigParser()
        self.config.add_section('podcast')
        self.config['podcast']['player'] = "mpv --no-video"

        if not os.path.isfile(self.user_config_path):
            with open(self.user_config_path, 'w') as f:
                self.config.write(f)

        self.config = configparser.ConfigParser()
        self.config.sections()
        self.config.read(self.user_config_path)

    def get_media_player(self):
        """
        Get the media player name

        Returns
        -------
        string
            the name of the media player of choice
        """
        return self.config['podcast']['player']

    def set_media_player(self, player_name):
        """
        Set the name of the media player of choice.

        Parameters
        ----------
        player_name : string
            The name of the media player of choice. mpv or mplayer
        """
        self.config.set('podcast','player',player_name)
        with open(self.user_config_path, 'w') as configfile:
            self.config.write(configfile)
