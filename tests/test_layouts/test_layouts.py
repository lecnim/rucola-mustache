import os
import unittest
from rucola import Rucola, compare_dirs
from rucola_mustache import MustacheLayouts


class Test(unittest.TestCase):
    """A rucola-mustache-layouts plugin"""

    def test(self):

        app = Rucola(os.path.dirname(__file__))
        app.clear_output()

        index = app.get('index.html')
        index['title'] = 'Index'
        index['view'] = 'main.html'

        app.use(
            MustacheLayouts(
                partials='partials',
                default='default/main.html',
                metadata_key='view'
            )
        )
        app.build()

        # Compare the content of a 'build' directory with an 'expected' one:

        self.assertTrue(
            compare_dirs(app.output, os.path.join(app.path, 'expected'))
        )
