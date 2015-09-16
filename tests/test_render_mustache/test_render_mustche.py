import unittest
from rucola import File
from rucola_mustache import render_mustache


class Test(unittest.TestCase):
    """A rucola-mustache plugin"""

    # Basic

    def test_string(self):

        x = render_mustache('{{ foo }}', context={'foo': 'banana'})
        self.assertEqual('banana', x)

    def test_file(self):

        f = File('test.html', content='{{ foo }}')

        x = render_mustache(f, context={'foo': 'banana'})
        self.assertEqual('banana', x)
        self.assertEqual('{{ foo }}', f.content)
