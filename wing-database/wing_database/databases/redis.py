import redis

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 6379
DEFAULLT_DB = 0


class RedisDatabase(object):
    def __init__(self, app, **kwargs):
        # TODO: connection parameters
        uri = kwargs.get('uri')
        host = kwargs.get('host', DEFAULT_HOST)
        port = kwargs.get('port', DEFAULT_PORT)
        db = kwargs.get('db', DEFAULT_DB)

        if uri:
            client = redis.from_url(uri, db=db)
        else:
            client = redis.Redis(host=host, port=port, db=db)

        self.db = client

    def get(self):
        return self.db
