import jinja2
import os


class SilentUndefined(jinja2.Undefined):
    def _fail_with_undefined_error(self, *args, **kwargs):
        return None


class Jinja2(object):
    def __init__(self, app, template_dir):
        self.app = app
        self.template_dir = template_dir
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.template_dir),
            undefined=SilentUndefined
        )

    def get_template(self, name):
        return self.env.get_template(name)
