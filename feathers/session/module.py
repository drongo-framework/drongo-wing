from .backend import RedisBackend

import uuid


SESSION_COOKIE = '_drongo_sessid'


class Session(object):
    def __init__(self, app, backend='redis', connection=None):
        self.app = app
        self.backend = None
        if backend == 'redis':
            self.backend = RedisBackend(app, connection)

    def load(self, request):
        sessid = request.cookies.get(SESSION_COOKIE, None) or uuid.uuid4().hex
        if self.backend is not None:
            request.context.session = self.backend.load(sessid)
            return request.context.session

    def save(self, request, response):
        if self.backend is not None:
            self.backend.save(request.context.session)
            response.set_cookie(SESSION_COOKIE, request.context.session._id)
