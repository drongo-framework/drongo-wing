from drongo import HttpStatusCodes, HttpResponseHeaders

from urllib.parse import urlencode

import requests
import uuid


class Facebook(object):
    def __init__(self, module, settings):
        self.module = module
        self.settings = settings

    def login_redirect(self, request, response, callback_url):
        params = urlencode({
            'client_id': self.settings['app_id'],
            'redirect_uri': callback_url,
            'auth_type': 'rerequest',
            'scope': 'email,public_profile'
        })
        url = 'https://www.facebook.com/v2.8/dialog/oauth?' + params
        response.set_status(HttpStatusCodes.HTTP_303)
        response.set_header(HttpResponseHeaders.LOCATION, url)
        response.set_content('')

    def callback(self, request, response, callback_url):
        if 'error' in request.query:
            self.module.auth_module.add_error_message(
                request, 'Social login deined!')
            return False

        # Get the access token
        params = urlencode({
            'client_id': self.settings['app_id'],
            'redirect_uri': 'http://localhost:8000' + callback_url,
        })
        url = 'https://graph.facebook.com/v2.8/oauth/access_token'
        params = {
            'client_id': self.settings['app_id'],
            'client_secret': self.settings['app_secret'],
            'redirect_uri': callback_url,
            'code': request.query['code'][0]
        }
        response = requests.get(url, params)
        access = response.json()

        if 'access_token' not in access:
            self.module.auth_module.add_error_message(
                request, 'Could not get the token!')
            return False

        # Get the profile
        url = 'https://graph.facebook.com/v2.8/me'
        params = {
            'access_token': access['access_token'],
            'fields': 'id,name,picture,email'
        }
        response = requests.get(url, params)
        profile = response.json()

        if 'email' not in profile:
            self.module.auth_module.add_error_message(
                request, 'Could not get fetch the Email ID!')
            return False

        username = profile.get('email')
        if not self.module.auth_module.user_exists(username):
            self.module.auth_module.create_user(
                username, uuid.uuid4().hex, True)

        self.module.auth_module.update_user(
            username=username,
            fields={
                'social_auth.' + self.settings['name'] + '.access_token':
                    access['access_token'],
                'name': profile['name'],
            }
        )

        self.module.auth_module.authenticate_user(request, response,
                                                  profile.get('email'))
        return True
