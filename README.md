# SudokuSAT
Solves Sudoku puzzles of size 4, 9 or 16 using a basic DPLL SAT.

It implements a few strategies for branching, which can be selected as an optional command line argument (``-S`` or ``--strategy``). If none is specified, it defaults to no strategy.

It reads 2 types of inputs:
1. A DIMACS file containing 1 SUDOKU, with both rules and puzzle
This is simply a generic SAT solver with input in DIMACS.

Example:

    python -S2 SAT.py input/sudokus/sudoku0.txt

2. A file containing an arbitrary number of same-size SUDOKU puzzles, each on one line,
where each character is either a digit (initial position) or a dot (empty).
The size of the sudoku is inferred from the number of chars ``n`` in the first line and rules are fetched from ``input/sudoku-rules-<n>x<n>.txt``
To allow this batch mode, add the argument ``-a`` (``--all``).

    python -S3 SAT.py input/sudokus/4x4.txt

It outputs the truth assignment as the list of symbols that are positive. If option 2 is used, all outputs are in the same file on separate lines.

A separate script to generate standalone rules + puzzle DIMACS SUDOKU files from the dot-file input. You can generate as many separate files as specified by the argument ``-n``

    python generate_dimacs_puzzle.py -n 1 input/sudokus/4x4.txt

This will generate ``sudoku0.txt...sudoku<n-1>.txt`` of separate DIMACS rules+puzzle.

To run unit tests:

  python -m sudoku.solver.test_sat_solver
  python -m sudoku.dimacs.test_parse
