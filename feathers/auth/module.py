from drongo import HttpResponseHeaders, HttpStatusCodes

from .actions import AuthActions
from .backend import AuthMongoBackend
from .views import AuthViews


class Auth(object):
    def __init__(self, app, backend='mongo', base_url='auth',
                 api_base_url='/api/auth', connection=None):
        self.app = app
        self.base_url = base_url
        self.api_base_url = api_base_url

        if backend == 'mongo':
            self.backend = AuthMongoBackend(connection)

        self.views = AuthViews(self)
        self.actions = AuthActions(self)
