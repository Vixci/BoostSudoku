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
        self.assertEqual(dlis(generic_clauses_1), 3)
        self.assertEqual(dlis(generic_clauses_2), 3)
        self.assertEqual(dlis(generic_clauses_3), 1)
        self.assertEqual(dlis([{},{}]), None)

    def test_jw(self):
        self.assertEqual(jw(generic_clauses_1), 3)
        self.assertEqual(jw(generic_clauses_2), 3)
        self.assertEqual(jw(generic_clauses_3), 1)
        self.assertEqual(jw([{},{}]), None)

    def test_jw2(self):
        self.assertEqual(jw2(generic_clauses_1), -1)
        self.assertEqual(jw2(generic_clauses_2), 3)
        self.assertEqual(jw2(generic_clauses_3), 1)
        self.assertEqual(jw2([{},{}]), None)

if __name__ == '__main__':
    unittest.main()
    print("All tests passed")
