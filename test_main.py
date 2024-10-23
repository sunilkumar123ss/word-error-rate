import unittest
try:
    from .main import evaluate
except ImportError:
    from main import evaluate

class WerTests(unittest.TestCase):

    def test_normalization(self):
        self.assertEqual(evaluate('HELLO, world!', 'hello world')['wer'], 0)

    def test_substitution_and_deletion(self):
        r = evaluate('a b c d', 'a x d')
        self.assertEqual((r['substitutions'], r['deletions'], r['insertions']), (1, 1, 0))
        self.assertEqual(r['wer'], 0.5)

    def test_insertion_can_exceed_one(self):
        self.assertEqual(evaluate('a', 'a b c')['wer'], 2)
