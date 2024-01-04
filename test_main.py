import unittest
try:
    from .main import evaluate
except ImportError:
    from main import evaluate

class WerTests(unittest.TestCase):

    def test_normalization(self):
        self.assertEqual(evaluate('HELLO, world!', 'hello world')['wer'], 0)
