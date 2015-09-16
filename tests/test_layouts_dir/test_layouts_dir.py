import os
import unittest
from rucola import Rucola
from rucola_mustache import MustacheLayouts


class Test(unittest.TestCase):
    """A rucola-mustache-layouts plugin"""

    def test(self):

        app = Rucola(os.path.dirname(__file__))
        app.clear_output()

        f = app.get('test.html')
        f['layout'] = 'main.html'

        app.use(
            MustacheLayouts(source='templates')
        )

        self.assertEqual('Hello Rucola!', f.content)
