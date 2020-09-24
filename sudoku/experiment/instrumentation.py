from time import time
from functools import reduce
import os

# Dimensions
_sudoku_size = 0
_strategy = 0
_number_of_initial_clauses = 0

# Metrics
_start_time = 0
_count_time = 0
_count_backtracks = 0
_count_branches = 0
_counter_filename = "counterfile.csv"
_number_of_solved_unit_clauses = 0
_number_of_solved_pure_literals = 0

def seconds_to_str(t):
    return "%d:%02d:%02d.%03d" % \
           reduce(lambda ll, b: divmod(ll[0], b) + ll[1:],
                  [(t * 1000,), 1000, 60, 60])

def initialize_counter_file(filename):
    global _counter_filename
    fileparts = filename[::-1].split('.', 1)
    _counter_filename = fileparts[1][::-1] + ".csv"
    if os.path.exists(_counter_filename):
        os.remove(_counter_filename)

def end_counters():
    global _count_time
    _count_time = time() - _start_time

def start_counters(symbols_size, strategy, number_of_initial_clauses):
    global _sudoku_size
    global _symbols_size
    global _strategy
    global _number_of_initial_clauses
    global _start_time
    global _count_backtracks
    global _count_branches
    global _number_of_initial_clauses
    global _number_of_solved_unit_clauses
    global _number_of_solved_pure_literals
    global _has_multiple_solutions

    _symbols_size = symbols_size
    _sudoku_size = 4 if symbols_size <=64 else 9 if symbols_size <= 729 else 16
    _strategy = strategy
    _number_of_initial_clauses = number_of_initial_clauses
    _start_time = time()
    _count_backtracks = 0
    _count_branches = 0
    _number_of_solved_unit_clauses = 0
    _number_of_solved_pure_literals = 0
    _has_multiple_solutions = False

def print_debug_counters():
    print("{}, {}, {}, {} \n".format(\
    _count_backtracks, _count_branches, \
    _number_of_solved_unit_clauses, _number_of_solved_pure_literals))

def check_has_multiple_solutions(solution_length):
    global _has_multiple_solutions
    # None: no solution, True: multiple solutions, False: one solution
    if solution_length == 0:
        _has_multiple_solutions = None
    elif solution_length < _symbols_size:
        _has_multiple_solutions = True
    else:
        _has_multiple_solutions = False

def incr_number_of_solved_unit_clauses(count_simplify):
    global _number_of_solved_unit_clauses
    _number_of_solved_unit_clauses = _number_of_solved_unit_clauses + count_simplify

def incr_number_of_solved_pure_literals(count_simplify):
    global _number_of_solved_pure_literals
    _number_of_solved_pure_literals = _number_of_solved_pure_literals + count_simplify

def incr_backtracks():
    global _count_backtracks
    _count_backtracks = _count_backtracks + 1

def incr_branches():
    global _count_branches
    _count_branches = _count_branches + 1

def save_counters():
    with open(_counter_filename, "a") as outfile:
        outfile.write("{}, {}, {}, {}, {}, {}, {}, {}, {}\n".format(\
        _sudoku_size, _strategy, _number_of_initial_clauses, \
        _count_time, seconds_to_str(_count_time), _count_backtracks, _count_branches, \
        _number_of_solved_unit_clauses,
        _has_multiple_solutions))
