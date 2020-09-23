from .heuristics import *
import unittest

generic_clauses_1 = [{1,-2},{-1,2,3},{1,3,4},{-1},{-1,3},{3}]
generic_clauses_2 = [{1,-3},{-1,2,3},{1,3,4},{-3},{-1,3},{3}]
generic_clauses_3 = [{1},{2},{-3}]

class TestSolveMethod(unittest.TestCase):
    def test_dlcs(self):
        self.assertEqual(dlcs(generic_clauses_1), -1)
        self.assertEqual(dlcs(generic_clauses_2), 3)
        self.assertEqual(dlcs(generic_clauses_3), 1)
        self.assertEqual(dlcs([{},{}]), None)

    def test_dlis(self):
        symbol, value = dlis(generic_clauses_1)
        self.assertEqual(symbol, 3)
        self.assertTrue(value)

    def test_jw(self):
        symbol, value = jw(generic_clauses_1)
        self.assertEqual(symbol, 3)
        self.assertTrue(value)

    def test_jw2(self):
        symbol, value = jw2(generic_clauses_1)
        self.assertEqual(symbol, 3)
        self.assertTrue(value)

if __name__ == '__main__':
    unittest.main()
    print("All tests passed")
