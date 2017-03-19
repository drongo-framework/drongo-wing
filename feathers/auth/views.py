class AuthViews(object):
    def __init__(self, auth):
        self.app = auth.app
        self.base_url = auth.base_url
        self.auth = auth
        self.init()

    def init(self):
        self.app.add_route(
            self.base_url + '/login', self.login)
        self.app.add_route(
            self.base_url + '/register', self.register)
        self.app.add_route(
            self.base_url + '/register/success', self.register_success)
        self.app.add_route(
            self.base_url + '/activate/failure', self.activation_failure)

    def before(self, request, response):
        request.context.modules.session.load(request)
        if 'messages' in request.context.session.auth:
            response.context.messages = request.context.session.auth.pop(
                'messages')
        response.context.update(request.context)

    def after(self, request, response):
        request.context.modules.session.save(request, response)

    def render(self, request, response, template):
        template = request.context.modules.jinja2.get_template(template)
        response.set_content(template.render(response.context))

    def login(self, request, response):
        self.before(request, response)
        self.render(request, response, 'auth/login.html')
        self.after(request, response)

    def register(self, request, response):
        self.before(request, response)
        self.render(request, response, 'auth/register.html')
        self.after(request, response)

    def register_success(self, request, response):
        self.before(request, response)
        self.render(request, response, 'auth/register-success.html')
        self.after(request, response)

    def activation_failure(self, request, response):
        self.before(request, response)
        self.render(request, response, 'auth/activate-failure.html')
        self.after(request, response)
