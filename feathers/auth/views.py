class AuthViews(object):
    def __init__(self, auth):
        self.app = auth.app
        self.base_url = auth.base_url
        self.auth = auth

        self.init()
        self.app.add_middleware(self)

    def init(self):
        self.app.add_route(
            self.base_url + '/login', self.login)
        self.app.add_route(
            self.base_url + '/register', self.register)
        self.app.add_route(
            self.base_url + '/register/success', self.register_success)
        self.app.add_route(
            self.base_url + '/activate/failure', self.activation_failure)

    def before(self, ctx):
        if 'messages' in ctx.session.auth:
            ctx.messages = ctx.session.auth.pop(
                'messages')

    def render(self, ctx, template):
        template = ctx.modules.jinja2.get_template(template)
        ctx.response.set_content(template.render(ctx))

    def login(self, ctx):
        self.render(ctx, 'auth/login.html.j2')

    def register(self, ctx):
        self.render(ctx, 'auth/register.html.j2')

    def register_success(self, ctx):
        self.render(ctx, 'auth/register-success.html.j2')

    def activation_failure(self, ctx):
        self.render(ctx, 'auth/activate-failure.html.j2')
