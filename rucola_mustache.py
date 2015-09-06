import os
import re
import pystache


class Mustache:

    def __init__(self, pattern='**/*.html', partials=None):
        self.pattern = pattern
        self.partials = partials

    def __call__(self, app):

        root = app.source if self.partials is None else self.partials
        r = pystache.Renderer(search_dirs=root)

        for f in app.find(self.pattern):
            f.content = r.render(f.content, f)
