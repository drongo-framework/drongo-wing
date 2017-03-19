from .backend import RedisBackend


class Session(object):
    def __init__(self, app, backend='redis', connection=None):
        self.app = app
        self.backend = None
        if backend == 'redis':
            self.backend = RedisBackend(app, connection)

    def load(self, request):
        if self.backend is not None:
            self.backend.load(request)

    def save(self, request, response):
        if self.backend is not None:
            self.backend.save(request, response)
