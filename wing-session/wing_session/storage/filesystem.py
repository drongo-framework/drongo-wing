from .common import DEFAULT

import os
import pickle
import uuid


class Filesystem(object):
    def __init__(self, **config):
        self.path = config.get('path')
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def load(self, session_id):
        session_file = os.path.join(self.path, session_id)
        if os.path.exists(session_file):
            with open(session_file, 'rb') as fd:
                session = pickle.load(fd)
        else:
            session_id = uuid.uuid4().hex
            session = pickle.loads(DEFAULT)

        session._sessid = session_id
        return session

    def save(self, session):
        session_file = os.path.join(self.path, session._sessid)
        with open(session_file, 'wb') as fd:
            pickle.dump(session, fd)
