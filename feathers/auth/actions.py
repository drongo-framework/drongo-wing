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

    def login_do(self, ctx):
        try:
            username = ctx.request.query.get('username')[0]
            password = ctx.request.query.get('password')[0]
            self.module.verify_login(username, password)
            self.module.authenticate_user(ctx, username)

            if 'next' in ctx.request.query:
                redirect_url = ctx.request.query.get('next')[0]
            else:
                redirect_url = '/'
            ctx.response.set_redirect(redirect_url)

        except Exception as e:
            self.module.add_error_message(ctx, str(e))
            ctx.response.set_redirect(self.base_url + '/login')

    def logout_do(self, ctx):
        self.module.logout(ctx)

        if 'next' in ctx.request.query:
            redirect_url = ctx.request.query.get('next')[0]
        else:
            redirect_url = '/'

        ctx.response.set_redirect(redirect_url)

    def register_do(self, ctx):
        try:
            username = ctx.request.query.get('username')[0]
            password = ctx.request.query.get('password')[0]
            self.module.create_user(username, password)
            self.response.set_redirect(self.base_url + '/register/success')

        except Exception as e:
            self.module.add_error_message(ctx, str(e))
            self.response.set_redirect(self.base_url + '/register')

    def activate_do(self, ctx):
        try:
            username = ctx.request.query.get('username')[0]
            code = ctx.request.query.get('code')[0]
            self.backend.activate_user(username, code)
            ctx.response.set_redirect(self.base_url + '/login')

        except Exception as e:
            self.module.add_error_message(str(e))
            self.response.set_redirect(self.base_url + '/activate/failure')
