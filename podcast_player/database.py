from sqlobject import SQLObject, StringCol

class PodcastDatabase(SQLObject):
    """A database of podcast names and urls."""    
    name = StringCol()
    url = StringCol()