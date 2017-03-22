from drongo.utils import dict2

import pickle


DEFAULT = pickle.dumps(dict2())


class Backend(object):
    pass


class RedisBackend(Backend):
    def __init__(self, app, connection):
        self.app = app
        self.connection = connection

    def load(self, session_id):
        session = pickle.loads(self.connection.get(session_id) or DEFAULT)
        session._id = session_id
        return session

    def save(self, session):
        self.connection.set(session._id, pickle.dumps(session))
