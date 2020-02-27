from podcast_player.database_manager import PodcastDatabaseManager
from podcast_player.podcast_parser import PodcastParser
from podcast_player.user_settings import UserSettings
import os
import sys
from PyInquirer import prompt

class PodcastPlayer(object):

    def __init__(self, debug_=False):
        self._database_manager = PodcastDatabaseManager(debug_=debug_)
        self._podcast_parser = PodcastParser(debug_=debug_)
        self.debug_ = debug_

    def add_podcast(self, url):
        """
        Add a podcast

        Parameters
        ----------
        url : string
            The URL of the podcast to subscribe to.
        """
        podcast = self._podcast_parser.create_podcast_from(url)
        self._database_manager.add_podcast(podcast)
                
    def import_opml(self, opml_file):
        """
        Import feeds from an opml file
        
        Parameters
        ----------
        opml_file : string
            The relative path to the opml file that we want to import. 
        """
        for podcast in self._podcast_parser.generate_feeds_from(opml_file):
            self._database_manager.add_podcast(podcast)

    def handle_choice(self, answers, key):
        """
        Handle user input
        """
        # if there is no input then the user probably ctrl+c'ed out
        if len(answers) == 0:
            sys.exit(0)
        
        # handle the back and quit
        inp = answers[key]
        if inp == "Back":
            self.main_menu()
        elif inp == "Quit":
            sys.exit(0)

    def delete_podcast_menu(self):
        """
        The delete menu
        Here we list all the podcasts that the user is subscribed to
        and allow the user to choose which one they want to delete
        """
        podcasts = self._database_manager.get_all_subscribed_podcasts()
        
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
                'message': 'Select the podcasts you wish to delete and then press enter/return',
                'choices': podcast_names
            }
        ]

        answers = prompt(questions)
        self.handle_choice(answers, 'podcasts')
        podcasts = answers["podcasts"]     
        self._database_manager.delete(podcasts)

    def set_player(self, player):
        """
        Save the preferred media player in the user settings

        Parameters
        ----------
        player : string
            The player that we pass the media url to when we play a podcast.
        """
        user_settings = UserSettings()
        user_settings.set_media_player(player)

    def play_podcast(self, url):
        """
        Play the podcast using the user's preferred player
        """
        user_settings = UserSettings()
        player = user_settings.get_media_player()
        os.system('clear')
        os.system(player + " "+ url)

    def episode_menu(self, podcast):
        """
        The episode menu
        Here we list all the episodes of the selected podcast
        and allow the user to choose which one they want to listen to

        Parameters
        ----------
        podcast : PodcastDatabase
            The podcast entry from the database
        """
        entries = []
        titles = []
        # NB: podcast entries are already sorted per decreasing published date per construction
        for podcast_entry in self._podcast_parser.generate_feed_entries_from(podcast.url, self.debug_):
            entries.append(podcast_entry)
            titles.append("{}".format(podcast_entry))
        
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
        self.handle_choice(answers, 'episode')

        choice = titles.index(answers["episode"])
        chosen_podcast_entry = entries[choice]
        url_to_play = chosen_podcast_entry.get_episode_media_url()

        if type(url_to_play) is str:
            self.play_podcast(url_to_play)
        self.episode_menu(podcast)   
     
    def main_menu(self):
        """
        The main menu
        Here we list all the podcasts that the user is subscribed to
        and allow the user to choose which one they want to see the episodes of
        At that point we move to the episode menu
        """
        podcasts = self._database_manager.get_all_subscribed_podcasts()
        
        if podcasts.count() == 0:
            print("There are no podcast feeds found.")
            print("To add a podcast use the 'add' parameter:\n")
            print("podcast add http://www.mypodcast.com/feed.rss\n")
            sys.exit(0)
        
        podcast_names = []

        for index, podcast in enumerate(podcasts):
            podcast_names.append(podcast.name)

        print (podcast_names)
        
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
        self.handle_choice(answers,'podcast')

        chosen_podcast = self._database_manager.get_matching_podcast(answers["podcast"])
        self.episode_menu(chosen_podcast)
