import os
import glob
import pystache


def render_mustache(template, context=None, partials=None):

    if isinstance(partials, str):
        partials = PartialsReader(partials)
    elif partials is None:
        partials = {}

    renderer = pystache.Renderer(partials=partials, file_extension=False)
    return renderer.render(template, context)


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


class MustacheLayouts:

    def __init__(self, pattern='**/*.html', source='layouts',
                 partials=None, default=None, metadata_key='layout'):

        self.pattern = pattern
        self.source = source
        self.default_layout = default
        self.metadata_key = metadata_key
        self.partials = partials

    def __call__(self, app):

        if self.partials:
            pf = PartialsReader(os.path.join(app.path, self.partials))
        else:
            pf = {}

        for f in app.find(self.pattern):

            layout_path = f.get(self.metadata_key, self.default_layout)
            if layout_path:

                # On windows: a/b => a\\b
                layout_path = os.path.normpath(layout_path)
                # path/to/app/ + layouts/ + something.html
                path = os.path.join(app.path, self.source, layout_path)

                with open(path) as fp:
                    layout_content = fp.read()

                f.content = render_mustache(layout_content, f, partials=pf)
