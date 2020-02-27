import unittest
from podcast_player.podcast import PodcastEntry
from datetime import datetime, timedelta

class TestPodcastEntry(unittest.TestCase):
    """
    Test compute_relative_readable_published_date() on a podcast entry with a published date set to 14th May 2020.
    """

    def setUp(self):
        self.published_date = datetime(2020, 5, 14)
        self.podcast_entry = PodcastEntry(published_date=self.published_date, title='dummy_title', episode_media_url='dummy_url')        

    def test_compute_relative_readable_published_date_when_published_today_should_return_today(self):
        self.assertEqual(self.podcast_entry.compute_relative_readable_published_date(
            reference_date=self.published_date.date(), verbose = True), 
            "today")

    def test_compute_relative_readable_published_date_when_published_yesterday_but_less_than_one_day_should_return_one_day_ago(self):
        self.published_date = datetime(2020, 5, 14, 20, 00)
        self.assertEqual(self.podcast_entry.compute_relative_readable_published_date(
            reference_date=datetime(2020, 5, 15).date(), verbose = True), 
            "1 day ago")

    def test_compute_relative_readable_published_date_when_published_yesterday_should_return_one_day_ago(self):
        self.assertEqual(self.podcast_entry.compute_relative_readable_published_date(
            reference_date=self.published_date + timedelta(days=1), verbose = True), 
            "1 day ago")
    
    def test_compute_relative_readable_published_date_when_published_last_month_should_return_one_month_ago(self):
        self.assertEqual(self.podcast_entry.compute_relative_readable_published_date(
            reference_date=self.published_date + timedelta(days=31), verbose = True), 
            "1 month ago")
    
    def test_compute_relative_readable_published_date_when_published_last_year_should_return_one_year_ago(self):
        self.assertEqual(self.podcast_entry.compute_relative_readable_published_date(
            reference_date=self.published_date + timedelta(days=365), verbose = True), 
            "1 year ago")
    
    def test_compute_relative_readable_published_date_when_published_less_than_a_month_ago_should_return_the_number_of_days_ago(self):
        self.assertEqual(self.podcast_entry.compute_relative_readable_published_date(
            reference_date=self.published_date + timedelta(days=25), verbose = True), 
            "25 days ago")
    
    def test_compute_relative_readable_published_date_when_published_more_than_a_month_ago_should_return_a_month_and_the_remaining_days_ago(self):
        self.assertEqual(self.podcast_entry.compute_relative_readable_published_date(
            reference_date=self.published_date + timedelta(days=38), verbose = True), 
            "1 month 7 days ago")
    
    def test_compute_relative_readable_published_date_when_published_more_than_a_year_ago_should_return_a_year_and_remaining_months_and_days_ago(self):
        self.assertEqual(self.podcast_entry.compute_relative_readable_published_date(
            reference_date=self.published_date + timedelta(days=430), verbose = True), 
            "1 year 2 months 4 days ago")

if __name__ == '__main__':
    unittest.main()
