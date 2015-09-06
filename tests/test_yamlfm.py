import os
import unittest
from rucola import Rucola
from rucola_mustache import Mustache


class Test(unittest.TestCase):

    def setUp(self):
        self.app = Rucola(os.path.dirname(__file__))

    def test_basic(self):

        f = self.app.get('foo.html')
        f['var'] = 'banana'

        self.app.use(
            Mustache()
        )

        self.assertEqual('banana', f.content)

    def test_partials(self):

        f = self.app.get('basket.html')
        f['fruits'] = ['apple, ', 'banana']

        self.app.use(
            Mustache(partials='partials')
        )

        self.assertEqual('hello', self.app.get('partials.html').content)

        self.assertEqual('apple, banana', self.app.get('basket.html').content)

    def test_no_partials(self):

        self.app.use(
            Mustache()
        )
        self.assertEqual('src', self.app.get('partials.html').content)




    # def test_custom_limiter(self):
    #
    #     self.app.use(
    #         YamlFrontmatter(limiter='===')
    #     )
    #
    #     f = self.app.get('limiter.md')
    #     self.assertEqual('yes', f['test'])
    #     self.assertEqual('content', f.content)
    #
    # def test_no_content(self):
    #
    #     self.app.use(
    #         YamlFrontmatter('nocontent.md')
    #     )
    #
    #     f = self.app.get('nocontent.md')
    #     self.assertEqual('', f.content)
