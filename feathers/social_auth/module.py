from drongo import HttpStatusCodes, HttpResponseHeaders

from urllib.parse import urlencode

import requests

from .providers.fb import Facebook


class SocialAuth(object):
    def __init__(self, app, base_url='/auth/social', settings=[],
                 auth_module=None):
        self.app = app
        self.base_url = base_url
        self.settings = settings
        self.auth_module = auth_module
        self.init()

    def init(self):
        self.providers = {}
        for setting in self.settings:
            if setting['provider'] == 'facebook':
                self.providers[setting['name']] = Facebook(self, setting)

        self.app.add_route(
            self.base_url + '/{name}/begin', self.login)
        self.app.add_route(
            self.base_url + '/{name}/callback', self.callback)

    def before(self, request, response):
        request.context.modules.session.load(request)

    def after(self, request, response):
        request.context.modules.session.save(request, response)

    def redirect(self, response, url):
        response.set_status(HttpStatusCodes.HTTP_303)
        response.set_header(HttpResponseHeaders.LOCATION, url)
        response.set_content('')

    def login(self, request, response, name):
        provider = self.providers.get(name)
        callback_url = self.base_url + '/' + name + '/callback'
        # FIXME: Hardcoded url
        provider.login_redirect(request, response,
                                'http://localhost:8000' + callback_url)

    def callback(self, request, response, name):
        self.before(request, response)
        provider = self.providers.get(name)
        callback_url = self.base_url + '/' + name + '/callback'
        # FIXME: Hardcoded url
        result = provider.callback(request, response,
                                   'http://localhost:8000' + callback_url)
        self.after(request, response)
        if result:
            self.redirect(response, '/')
        else:
            self.redirect(response, '/auth/login')
