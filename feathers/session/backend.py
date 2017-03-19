from drongo.utils import dict2

import pickle
import uuid


DEFAULT = pickle.dumps(dict2())
SESSION_COOKIE = '_drongo_sessid'


class Backend(object):
    pass


class RedisBackend(Backend):
    def __init__(self, app, connection):
        self.app = app
        self.connection = connection

    def load(self, request):
        sessid = request.cookies.get(SESSION_COOKIE, None) or uuid.uuid4().hex
        request.context.session = pickle.loads(self.connection.get(sessid)
                                               or DEFAULT)
        request.context.session._id = sessid

    def save(self, request, response):
        session = request.context.session
        self.connection.set(session._id, pickle.dumps(session))
        response.set_cookie(SESSION_COOKIE, session._id)
