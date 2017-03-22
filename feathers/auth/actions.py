from drongo import HttpResponseHeaders, HttpStatusCodes
from drongo.utils import dict2


class AuthActions(object):
    def __init__(self, module):
        self.app = module.app
        self.module = module
        self.base_url = module.base_url
        self.init()

    def init(self):
        self.app.add_route(
            self.base_url + '/login/do', self.login_do, 'POST')
        self.app.add_route(
            self.base_url + '/logout/do', self.logout_do, 'GET')
        self.app.add_route(
            self.base_url + '/register/do', self.register_do, 'POST')
        self.app.add_route(
            self.base_url + '/activate/do', self.activate_do, 'GET')

    def redirect(self, response, url):
        response.set_status(HttpStatusCodes.HTTP_303)
        response.set_header(HttpResponseHeaders.LOCATION, url)
        response.set_content('')

    def before(self, request, response):
        request.context.modules.session.load(request)

    def after(self, request, response):
        request.context.modules.session.save(request, response)

    def login_do(self, request, response):
        assert request.method == 'POST'
        self.before(request, response)

        try:
            username = request.query.get('username')[0]
            password = request.query.get('password')[0]
            self.module.verify_login(username, password)
            self.module.authenticate_user(request, response, username)

            if 'next' in request.query:
                redirect_url = request.query.get('next')[0]
            else:
                redirect_url = '/'
            self.redirect(response, redirect_url)

        except Exception as e:
            self.module.add_error_message(request, str(e))
            self.redirect(response, self.base_url + '/login')
        self.after(request, response)

    def logout_do(self, request, response):
        assert request.method == 'GET'
        self.before(request, response)

        self.module.logout(request)

        if 'next' in request.query:
            redirect_url = request.query.get('next')[0]
        else:
            redirect_url = '/'

        self.redirect(response, redirect_url)

        self.after(request, response)

    def register_do(self, request, response):
        assert request.method == 'POST'
        self.before(request, response)

        try:
            username = request.query.get('username')[0]
            password = request.query.get('password')[0]
            self.module.create_user(username, password)
            self.redirect(response, self.base_url + '/register/success')

        except Exception as e:
            self.module.add_error_message(request, str(e))
            self.redirect(response, self.base_url + '/register')

        self.after(request, response)

    def activate_do(self, request, response):
        assert request.method == 'GET'
        self.before(request, response)

        try:
            username = request.query.get('username')[0]
            code = request.query.get('code')[0]
            self.backend.activate_user(username, code)
            self.redirect(response, self.base_url + '/login')

        except Exception as e:
            request.context.session.auth.messages.error = [
                str(e)
            ]
            self.redirect(response, self.base_url + '/activate/failure')

        self.after(request, response)
