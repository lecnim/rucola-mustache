import os
import unittest
from rucola import Rucola
from rucola_mustache import Mustache


class Test(unittest.TestCase):
    """A rucola-mustache plugin"""

    def setUp(self):
        self.app = Rucola(os.path.dirname(__file__))

    # Basic

    def test_render_path(self):

        app = Rucola()
        app.create('url.html', content='My path: {{ path }}')
        app.create('url2.html', content='My path: {{ path }}')
        app.use(
            Mustache('url.html')
        )

        self.assertEqual('My path: url.html', app.get('url.html').content)
        self.assertEqual('My path: {{ path }}', app.get('url2.html').content)

    def test_default_pattern(self):
        """Should render all html files if a pattern argument is missing"""

        app = Rucola()
        app.create('url.html', content='My path: {{ path }}')
        app.create('hello.html', content='My path: {{ path }}')
        app.create('post.md', content='My path: {{ path }}')
        app.use(
            Mustache()
        )

        self.assertEqual('My path: url.html', app.get('url.html').content)
        self.assertEqual('My path: hello.html', app.get('hello.html').content)
        self.assertEqual('My path: {{ path }}', app.get('post.md').content)

    # Files metadata

    def test_file_metadata(self):

        app = Rucola()
        f = app.create('foo.html', content='{{ var }}')
        f['var'] = 'hello'
        app.use(
            Mustache()
        )

        self.assertEqual('hello', app.get('foo.html').content)

    def test_metadata_to_file(self):

        app = Rucola()
        a = app.create('a.html', content='A')
        b = app.create('b.html', content='{{ var.content }}')
        b['var'] = a
        app.use(
            Mustache()
        )

        self.assertEqual('A', app.get('a.html').content)

    # Argument metadata

    def test_metadata(self):

        app = Rucola()
        app.create('hello.html', content='{{ a }}, {{ path }}')
        app.use(
            Mustache(metadata={'a': 'Welcome', 'path': 'foo/bar'})
        )

        f = app.get('hello.html')
        self.assertEqual('Welcome, foo/bar', f.content)
        self.assertIsNone(f.get('a'))
        self.assertEqual('hello.html', f.path)

    # Argument partials

    def test_no_partials(self):

        app = Rucola(os.path.dirname(__file__))
        app.use(
            Mustache()
        )

        self.assertEqual('Using ', app.get('partials.html').content)

    def test_partials_path(self):

        app = Rucola(os.path.dirname(__file__))
        app.use(
            Mustache(partials='partials')
        )

        self.assertEqual('Using hello /partials', app.get('partials.html').content)

    def test_partials_name_conflict(self):

        app = Rucola(os.path.dirname(__file__))
        app.create('conflict.html', content='{{> same/foo }}')

        app.use(
            Mustache(partials='partials')
        )

        self.assertEqual('test', app.get('conflict.html').content)

    def test_partials_object(self):

        app = Rucola()
        f = app.create('foo.html', content='{{# list }}{{> shout }}{{/ list }}')
        f['list'] = ['dog', 'cat', 'bee']

        app.use(
            Mustache(partials={'shout': '{{.}}! '})
        )

        self.assertEqual('dog! cat! bee! ', app.get('foo.html').content)
