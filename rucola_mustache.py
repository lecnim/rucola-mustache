import os
import glob
import pystache


class PartialsReader:
    """Finds partials files, regardless of a file extension.
    For example {{> next }} will match 'next.mustache', 'next.html', 'next.something' etc.

    Content of the found partial is cached for a later use.
    """

    def __init__(self, path):
        self.path = path
        self.partials = {}

    def get(self, key):

        if key in self.partials:
            return self.partials[key]

        result = glob.glob(os.path.join(self.path, os.path.normpath(key)) + '.*')
        if result:

            if len(result) > 1:
                pass
                # TODO: Warn about pattens filenames conflict!

            with open(result[0]) as f:
                self.partials[key] = f.read()

            return self.partials[key]


class Mustache:

    def __init__(self, pattern='**/*.html', metadata=None, partials=None):

        self.pattern = pattern
        self.metadata = metadata
        self.partials = partials

    def __call__(self, app):

        if self.partials is None:
            pf = {}
        elif isinstance(self.partials, str):
            pf = PartialsReader(os.path.join(app.path, self.partials))
        else:
            pf = self.partials

        for f in app.find(self.pattern):

            if self.metadata:
                data = f.copy()
                data.update(self.metadata)
            else:
                data = f

            f.content = render_mustache(f.content, data, partials=pf)


def render_mustache(template, context=None, partials=None):

    if isinstance(partials, str):
        partials = PartialsReader(partials)
    elif partials is None:
        partials = {}

    renderer = pystache.Renderer(partials=partials, file_extension=False)
    return renderer.render(template, context)
