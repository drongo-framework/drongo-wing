import pymongo

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 27017


class MongoDatabase(object):
    def __init__(self, app, **kwargs):
        uri = kwargs.get('uri')
        host = kwargs.get('host', DEFAULT_HOST)
        port = kwargs.get('port', DEFAULT_PORT)
        name = kwargs.get('name')
        if uri:
            client = pymongo.MongoClient(kwargs.get('uri'))
        else:
            client = pymongo.MongoClient(host, port)
        self.db = client[name]
