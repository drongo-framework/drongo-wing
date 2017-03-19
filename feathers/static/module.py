from drongo import HttpResponseHeaders

from datetime import datetime, timedelta

import mimetypes
import os


class Static(object):
    def __init__(self, app, root_dir, base_url='/static', age=300):
        self.app = app
        self.root_dir = root_dir
        self.base_url = base_url
        self.age = age

        self.init()

    def init(self):
        self.app.add_route(
            self.base_url + '/{a}', self.serve_file)
        self.app.add_route(
            self.base_url + '/{a}/{b}', self.serve_file)
        self.app.add_route(
            self.base_url + '/{a}/{b}/{c}', self.serve_file)
        self.app.add_route(
            self.base_url + '/{a}/{b}/{c}/{d}', self.serve_file)
        self.app.add_route(
            self.base_url + '/{a}/{b}/{c}/{d}/{e}', self.serve_file)
        self.app.add_route(
            self.base_url + '/{a}/{b}/{c}/{d}/{e}/{f}', self.serve_file)

    def serve_file(self, request, response,
                   a=None, b=None, c=None, d=None, e=None, f=None):
        path = self.root_dir
        parts = [a, b, c, d, e, f]
        for part in parts:
            if part is not None:
                path = os.path.join(path, part)

        if os.path.exists(path) and not os.path.isdir(path):
            response.set_header(HttpResponseHeaders.CACHE_CONTROL,
                                'max-age=%d' % self.age)

            expires = datetime.utcnow() + timedelta(seconds=(self.age))
            expires = expires.strftime('%a, %d %b %Y %H:%M:%S GMT')
            response.set_header(HttpResponseHeaders.EXPIRES, expires)

            ctype = mimetypes.guess_type(path)[0] or 'application/octet-stream'
            response.set_header(HttpResponseHeaders.CONTENT_TYPE, ctype)

            with open(path, 'rb') as fd:
                return fd.read()
        return path
