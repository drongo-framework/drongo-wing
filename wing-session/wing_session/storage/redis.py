from drongo.utils import dict2

import pickle
import uuid


DEFAULT = pickle.dumps(dict2())


class Redis(object):
    def __init__(self, **config):
        self.db = config.get('db')

    def load(self, session_id):
        sess = self.db.get(session_id)
        if sess:
            session = pickle.loads(sess)
        else:
            session = pickle.loads(DEFAULT)
            session._sessid = uuid.uuid4().hex

        return session

    def save(self, session):
        self.db.set(session._sessid, pickle.dumps(session))
