import datetime
from dateutil.relativedelta import relativedelta

class Podcast(object):
    """
    Podcast model.
    """

    def __init__(self, url, title=""):
        self.url = url
        self.title = title
        # NB: not needed in current model to bind to the podcast entries
    
    def __str__(self): 
        return "{0}|{1}".format(self.title, self.url)

class PodcastEntry(object):
    """
    Podcast entry.
    """

    def __init__(self, title, published_date, episode_media_url, debug_=False):
        self.title = title
        self.published_date = published_date
        self.relative_readable_published_date = self.compute_relative_readable_published_date(verbose=debug_)
        self.episode_media_url = episode_media_url
    
    def get_episode_media_url(self):
        return self.episode_media_url
    
    def __str__(self): 
        """
        Readable entry to be displayed in the choice list.
        """
        return "{0} [{1}]".format(self.title, self.relative_readable_published_date if hasattr(self, "relative_readable_published_date") else '')

    def compute_relative_readable_published_date(self, reference_date = datetime.date.today(), verbose=False):
        """
        Compute a relative published date w.r.t. reference date.

        Parameters
        ----------
        reference_date : date object
        """
        relative_date = ""
        delta = relativedelta(reference_date, self.published_date.date())

        if self.published_date.date() == reference_date:
            relative_date = "today"
        elif (self.published_date + datetime.timedelta(days=1)).date() == reference_date:
            relative_date = "1 day ago"
        else:
            relative_date = "{0} year{1} ".format(delta.years, "s" if delta.years > 1 else "") if delta.years > 0 else relative_date
            relative_date += "{0} month{1} ".format(delta.months, "s" if delta.months > 1 else "") if delta.months > 0 else ''
            relative_date += "{0} day{1} ".format(delta.days, "s" if delta.days > 1 else "") if delta.days > 0 else ''
            relative_date += "ago" if relative_date != "today" else ""
        
        if verbose:
            print("Rel date: {0} (ref date: {1}, pub date: {2}, delta: [{3}])".format(relative_date, reference_date, self.published_date, delta))

        return relative_date
    


