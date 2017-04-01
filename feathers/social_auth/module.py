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
            self.base_url + '/{name}/begin', self.begin)
        self.app.add_route(
            self.base_url + '/{name}/callback', self.callback)

    def redirect(self, ctx, url):
        ctx.response.set_status(HttpStatusCodes.HTTP_303)
        ctx.response.set_header(HttpResponseHeaders.LOCATION, url)
        ctx.response.set_content('')

    def begin(self, ctx, name):
        provider = self.providers.get(name)
        callback_url = self.base_url + '/' + name + '/callback'
        # FIXME: Hardcoded url
        provider.login_redirect(ctx, 'http://localhost:8000' + callback_url)

    def callback(self, ctx, name):
        provider = self.providers.get(name)
        callback_url = self.base_url + '/' + name + '/callback'
        # FIXME: Hardcoded url
        result = provider.callback(ctx, 'http://localhost:8000' + callback_url)
        if result:
            self.redirect(ctx, '/')
        else:
            self.redirect(ctx, '/auth/login')
