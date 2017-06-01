
MONGO = 'MONGO'


class Database(object):
    def __init__(self, app, **kwargs):
        if kwargs.get('type') == MONGO:
            from .databases import MongoDatabase
            self.instance = MongoDatabase(app, **kwargs)
