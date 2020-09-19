from .parse import *
import unittest
from tempfile import TemporaryFile

sudoku_line_4 = "...3..4114..3..."
sudoku_dimacs_4 = """143 0
234 0
241 0
311 0
324 0
413 0
"""
sudoku_clauses_4 = [{'143'},{'234'},{'241'},{'311'},{'324'},{'413'}]

sudoku_symbols_4 = {'143', '234', '241', '311', '324', '413'}

sudoku_line_9 = "52...6.........7.13...........4..8..6......5...........418.........3..2...87....."
sudoku_dimacs_9 = """115 0
122 0
166 0
277 0
291 0
313 0
444 0
478 0
516 0
585 0
724 0
731 0
748 0
853 0
882 0
938 0
947 0
"""
sudoku_clauses_9 =[{'115'}, {'122'}, {'166'}, {'277'}, {'291'}, {'313'}, {'444'}, {'478'}, {'516'}, {'585'}, {'724'}, {'731'}, {'748'}, {'853'}, {'882'}, {'938'}, {'947'}]

sudoku_symbols_9 = {'115', '122', '166', '277', '291', '313', '444', '478', '516', '585', '724', '731', '748', '853', '882', '938', '947'}

sudoku_line_16 = "1.D....4.A58.....E.........C...G.2.76.GBF..4....39F.1A.D7........4.6.31...B.58.C8C7E.69..F.....D...D..........2...A.G8C....7E.1426.G4....57F.A...B..........8...F.....B..3A.42E1A.4C.5...E6.7.3........3D.C5.7B2....9..1GB.63.4.C...2.........6.....8FD.3....9.E"
sudoku_dimacs_16_partial ="""307 0
353 0
429 0
469 0
481 0
501 0
626 0
"""
sudoku_clauses_16_partial = [{'353'}, {'429'}, {'469'}, {'481'}, {'501'},{'626'}]
sudoku_symbols_16_partial = {'353', '429', '469', '481', '501', '626'}

generic_dimacs = """
c this is an example
p cnf 4 4
1 -2 0
2 3 0
1 3 4 0
-1 0
"""

generic_clauses = [{'1','-2'},{'2','3'},{'1','3','4'},{'-1'}]

generic_symbols = {'1','2','3','4'}

generic_dimacs_letters = """
c this is an example
p cnf 2 2
B -A 0
B 0
"""

generic_clauses_letters = [{'-A','B'},{'B'}]

generic_symbols_letters = {'A','B'}

class TestParseMethods(unittest.TestCase):

    def test_get_dimacs_string(self):
        self.assertEqual(get_dimacs_string(sudoku_line_4), sudoku_dimacs_4)
        self.assertEqual(get_dimacs_string(sudoku_line_9), sudoku_dimacs_9)
        self.maxDiff = None
        self.assertEqual(get_dimacs_string(sudoku_line_16)[:len(sudoku_dimacs_16_partial)], sudoku_dimacs_16_partial)

    def test_parse_puzzles(self):
        with TemporaryFile('w+') as f:
            f.write(sudoku_line_4)
            f.seek(0)
            sudoku_size, sudoku_clauses, sudoku_symbols = parse_sudoku_puzzles(f)
            self.assertEqual(sudoku_size, 4)
            self.assertEqual(sudoku_clauses[0], sudoku_clauses_4)
            self.assertEqual(sudoku_symbols, sudoku_symbols_4)

            f.truncate(0)
            f.seek(0)
            f.write(sudoku_line_9)
            f.seek(0)
            sudoku_size, sudoku_clauses, sudoku_symbols = parse_sudoku_puzzles(f)
            self.assertEqual(sudoku_size, 9)
            self.assertEqual(sudoku_clauses[0], sudoku_clauses_9)
            self.assertEqual(sudoku_symbols, sudoku_symbols_9)

            f.truncate(0)
            f.seek(0)
            f.write(sudoku_line_16)
            f.seek(0)
            sudoku_size, sudoku_clauses, sudoku_symbols = parse_sudoku_puzzles(f)
            self.assertEqual(sudoku_size, 16)
            self.assertTrue(all(x in sudoku_clauses[0] for x in sudoku_clauses_16_partial))
            self.assertTrue(sudoku_symbols_16_partial <= sudoku_symbols)

    def test_dimacs_to_cnf(self):
        clauses, symbols = dimacs_to_cnf(generic_dimacs)
        self.assertEqual(clauses, generic_clauses)
        self.assertEqual(symbols, generic_symbols)

        clauses, symbols = dimacs_to_cnf(generic_dimacs_letters)
        self.assertEqual(clauses, generic_clauses_letters)
        self.assertEqual(symbols, generic_symbols_letters)

        clauses, symbols = dimacs_to_cnf(sudoku_dimacs_4)
        self.assertEqual(clauses, sudoku_clauses_4)
        self.assertEqual(symbols, sudoku_symbols_4)

        clauses, symbols = dimacs_to_cnf(sudoku_dimacs_9)
        self.assertEqual(clauses, sudoku_clauses_9)
        self.assertEqual(symbols, sudoku_symbols_9)

        clauses, symbols = dimacs_to_cnf(sudoku_dimacs_16_partial)
        self.assertTrue(all(x in clauses for x in sudoku_clauses_16_partial));
        self.assertTrue(sudoku_symbols_16_partial <= symbols)


    def test_parse_sudoku_rules(self):
        with TemporaryFile('w+') as f:
            f.write(sudoku_line_4)
            f.seek(0)
            size4, _, symbols4 = parse_sudoku_puzzles(f)
            _, symbols_rules4 = parse_sudoku_rules(size4);
            self.assertTrue(symbols4 <= symbols_rules4)

            f.truncate(0)
            f.seek(0)
            f.write(sudoku_line_9)
            f.seek(0)
            size9, _, symbols9 = parse_sudoku_puzzles(f)
            _, symbols_rules9 = parse_sudoku_rules(size9);
            self.assertTrue(symbols9 <= symbols_rules9)

            f.truncate(0)
            f.seek(0)
            f.write(sudoku_line_16)
            f.seek(0)
            size16, _, symbols16 = parse_sudoku_puzzles(f)
            _, symbols_rules16 = parse_sudoku_rules(size16);
            self.assertTrue(symbols16 <= symbols_rules16)

if __name__ == '__main__':
    unittest.main()
    print("All parser tests passed")
