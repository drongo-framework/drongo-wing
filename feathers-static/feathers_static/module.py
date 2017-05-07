from drongo import HttpResponseHeaders

from functools import partial
from datetime import datetime, timedelta

import mimetypes
import os


class Static(object):
    def __init__(self, app, **config):
        self.app = app
        self.root_dir = config.get('root_dir')
        self.base_url = config.get('base_url', '/static')
        self.age = config.get('age', 300)
        self.max_depth = config.get('max_depth', 6)

        self.init()

    def init(self):
        self.app.add_url(
            pattern=self.base_url + '/{a}',
            method='GET',
            call=self.serve_file)
        self.app.add_url(
            pattern=self.base_url + '/{a}/{b}',
            method='GET',
            call=self.serve_file)
        self.app.add_url(
            pattern=self.base_url + '/{a}/{b}/{c}',
            method='GET',
            call=self.serve_file)
        self.app.add_url(
            pattern=self.base_url + '/{a}/{b}/{c}/{d}',
            method='GET',
            call=self.serve_file)
        self.app.add_url(
            pattern=self.base_url + '/{a}/{b}/{c}/{d}/{e}',
            method='GET',
            call=self.serve_file)
        self.app.add_url(
            pattern=self.base_url + '/{a}/{b}/{c}/{d}/{e}/{f}',
            method='GET',
            call=self.serve_file)

    def chunks(self, path):
        with open(path, 'rb') as fd:
            for chunk in iter(partial(fd.read, 102400), b''):
                yield chunk

    def serve_file(self, ctx,
                   a=None, b=None, c=None, d=None, e=None, f=None):
        path = self.root_dir
        parts = [a, b, c, d, e, f]
        for part in parts:
            if part is not None:
                path = os.path.join(path, part)

        if os.path.exists(path) and not os.path.isdir(path):
            ctx.response.set_header(HttpResponseHeaders.CACHE_CONTROL,
                                    'max-age=%d' % self.age)

            expires = datetime.utcnow() + timedelta(seconds=(self.age))
            expires = expires.strftime('%a, %d %b %Y %H:%M:%S GMT')
            ctx.response.set_header(HttpResponseHeaders.EXPIRES, expires)

            ctype = mimetypes.guess_type(path)[0] or 'application/octet-stream'

            ctx.response.set_header(HttpResponseHeaders.CONTENT_TYPE, ctype)
            ctx.response.set_content(self.chunks(path), os.stat(path).st_size)
            return

        return path
