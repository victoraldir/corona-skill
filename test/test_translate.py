import unittest
from translate import translator


class MyTestCase(unittest.TestCase):
    def test_something(self):

        country_translated = translator('pt', 'en-US', 'inglaterra')

        print(country_translated)
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
