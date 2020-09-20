#from sympy.logic.utilities.dimacs import load_file,load
from os.path import join
import math
import re

sudoku_rules_path = "input"

sudoku_rules = {
    4 : "sudoku-rules-4x4.txt",
    9 : "sudoku-rules-9x9.txt",
   16 : "sudoku-rules-16x16.txt"
}

# For SUDOKU-16, converts from 10-16 to A-G
def letter_gen(x):
    if x >= 10:
        return chr(ord('A') + x - 10)
    else:
        return str(x)

# For SUDOKU-16 converts from A-G to 10-16
def number_gen(tok):
    if tok in {'A','B','C','D','E','F','G'}:
        return int(ord(tok)-ord('A') + 10)
    return int(tok)

# Converts one line of dot format (one puzzle) into DIMACS
def get_dimacs_string(line):
    sudoku_string = ""
    cnt = 0
    sudoku_size =  math.isqrt(len(line))
    for tok in line:
        cnt += 1
        if tok.isalnum():
            r = (cnt - 1) // sudoku_size + 1
            c = cnt % sudoku_size if cnt % sudoku_size != 0 else sudoku_size
            v = number_gen(tok)
            pseudo_base = (sudoku_size + 1) if sudoku_size > 10 else 10
            sudoku_string += "{} 0\n".format(r * pseudo_base**2 + c * pseudo_base + v)
    return sudoku_string

def parse_whole_sudoku(dimacs_file):
    return False

# Gets the SUDOKU rules corresponding to the size as CNF clause
def parse_sudoku_rules(sudoku_size):
    return load_dimacs_file(join(sudoku_rules_path, sudoku_rules[sudoku_size]))

# Gets the puzzles from the file as SAT CNF clauses
def parse_sudoku_puzzles(puzzles_file):
    puzzles = []
    all_symbols = set()
    line = puzzles_file.readline()
    clauses, symbols = dimacs_to_cnf(get_dimacs_string(line))
    puzzles.append(clauses)
    all_symbols = all_symbols.union(symbols)
    puzzle_size = math.isqrt(len(line))

    for line in puzzles_file.readline():
        clauses, symbols = dimacs_to_cnf(get_dimacs_string(line))
        puzzles.append(clauses)
        all_symbols = all_symbols.union(symbols)
    return puzzle_size, puzzles, all_symbols

# Converts a string in DIMACS format to a CNF as a list of sets
# Does not validate DIMACS format, assumes input is correct
def dimacs_to_cnf(dimacs_string):
    clauses = []
    symbols = set()
    rows = dimacs_string.split('\n')
    # Exclude comments or summary
    exclusion_regex = re.compile('(c .*|p\s*cnf\s*(\d*)\s*(\d*))')

    for row in rows:
        if not exclusion_regex.match(row):
            literals = row.rstrip('0').split()
            clause = set()
            for literal in literals:
                clause.add(literal)
                symbols.add(literal.lstrip('-'))
            if len(clause) > 0:
                clauses.append(clause)
    return clauses, symbols

# Reads a DIMACS from a file into a CNF expression as a list of sets
def load_dimacs_file(filename):
    f = open(filename)
    content = f.read()
    f.close()
    return dimacs_to_cnf(content)
