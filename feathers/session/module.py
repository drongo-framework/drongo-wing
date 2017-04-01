import uuid


class Session(object):
    def __init__(self, app, **config):
        self.app = app
        self.backend = None

        backend = config.get('backend')
        if backend == 'redis':
            from .backends.redis import RedisBackend
            conn = config.get('connection')
            self.backend = RedisBackend(app, conn)

        self.cookie_name = config.get('cookie_name', '_drongo_sessid')
        app.add_middleware(self)

    def before(self, ctx):
        sessid = ctx.request.cookies.get(self.cookie_name, None) \
                    or uuid.uuid4().hex
        if self.backend is not None:
            ctx.session = self.backend.load(sessid)

    def after(self, ctx):
        if self.backend is not None:
            self.backend.save(ctx.session)
            ctx.response.set_cookie(self.cookie_name, ctx.session._id)
