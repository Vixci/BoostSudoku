import argparse
from sudoku.solver.sat_solver import solve_all, solve_one
from sudoku.dimacs.export import initialize_export_file
from sudoku.experiment.instrumentation import initialize_counter_file

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-S","--strategy", type=int, choices=range(0,5), default=-1, help="The strategy to use: S0 (no strategy), S1-S4")
    ap.add_argument("puzzle_filename", type=argparse.FileType('r'), help="the filename containing the SUDOKU puzzle / rules in DIMACS to be solved")
    ap.add_argument("-a", "--all", required=False, action='store_true', help= "If present, solves all the puzzles expressed in dot format present in the file and infers the rules from the size of the rows")
    args = vars(ap.parse_args())

    strategy = args['strategy']
    input_file = args['puzzle_filename']
    batch_mode = args['all']

    results_filename = initialize_export_file(input_file.name)
    initialize_counter_file(input_file.name)

    if strategy == -1:
        print("No strategy selected - all strategies will be trialed.")
        for strategy in range(0,5):
            execute(strategy, batch_mode, input_file, results_filename)
    else:
        execute(strategy, batch_mode, input_file, results_filename)

def execute(strategy, batch_mode, input_file, results_filename):
    if batch_mode:
        print("Solving all (batch mode) SUDOKUs using SAT with strategy {} on all {}...".format(strategy,input_file.name))
        solve_all(strategy,input_file, results_filename)
    else:
        print("Solving 1 SUDOKU using SAT with strategy {} on {}...".format(strategy,input_file.name))
        solve_one(strategy,input_file, results_filename)

if __name__ == "__main__":
    main()
