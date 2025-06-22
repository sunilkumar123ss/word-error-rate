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

    def test_empty_reference(self):
        self.assertEqual(evaluate('', '')['wer'], 0)
        self.assertIsNone(evaluate('', 'one')['wer'])
        self.assertEqual(evaluate('one', '')['deletions'], 1)

    def test_alignment_reconstructs_tokens(self):
        r = evaluate('a b c', 'a x c d')
        self.assertEqual([x['reference'] for x in r['alignment'] if x['reference'] is not None], ['a', 'b', 'c'])
        self.assertEqual([x['hypothesis'] for x in r['alignment'] if x['hypothesis'] is not None], ['a', 'x', 'c', 'd'])

    def test_invalid_or_oversized(self):
        with self.assertRaises(ValueError):
            evaluate(None, 'x')
        with self.assertRaises(ValueError):
            evaluate('a ' * 1001, '')
if __name__ == '__main__':
    unittest.main()
