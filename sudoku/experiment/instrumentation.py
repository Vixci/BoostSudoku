from time import time
from functools import reduce

# Dimensions
_sudoku_size = 0
_strategy = 0
_number_of_initial_clauses = 0

# Metrics
_start_time = 0
_count_time = 0
_count_backtracks = 0
_count_branches = 0

def seconds_to_str(t):
    return "%d:%02d:%02d.%03d" % \
           reduce(lambda ll, b: divmod(ll[0], b) + ll[1:],
                  [(t * 1000,), 1000, 60, 60])

def end_counters():
    global _count_time
    _count_time = time() - _start_time

def start_counters(symbols_size, strategy, number_of_initial_clauses):
    global _sudoku_size
    global _strategy
    global _number_of_initial_clauses
    global _start_time
    global _count_backtracks
    global _count_branches
    global _number_of_initial_clauses
    _sudoku_size = 4 if symbols_size <=64 else 9 if symbols_size <= 729 else 16
    _strategy = strategy
    _number_of_initial_clauses = number_of_initial_clauses
    _start_time = time()
    _count_backtracks = 0
    _count_branches = 0


def incr_backtracks():
    global _count_backtracks
    _count_backtracks = _count_backtracks + 1

def incr_branches():
    global _count_branches
    _count_branches = _count_branches + 1

def save_counters():
    with open("counterfile.csv", "a") as outfile:
        outfile.write("{}, {}, {}, {}, {}, {}\n".format(\
        _sudoku_size, _strategy, _number_of_initial_clauses, \
        seconds_to_str(_count_time), _count_backtracks, _count_branches))
