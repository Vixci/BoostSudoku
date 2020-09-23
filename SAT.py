import argparse
from sudoku.solver.sat_solver import solve_all, solve_one

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-S","--strategy", type=int, choices=range(0,5), default=-1, help="The strategy to use: S0 (no strategy), S1-S4")
    ap.add_argument("puzzle_filename", type=argparse.FileType('r'), help="the filename containing the SUDOKU puzzle / rules in DIMACS to be solved")
    ap.add_argument("-a", "--all", required=False, action='store_true', help= "If present, solves all the puzzles expressed in dot format present in the file and infers the rules from the size of the rows")
    args = vars(ap.parse_args())

    strategy = args['strategy']
    if strategy == -1:
        print("No strategy selected - all strategies will be trialed.")
        for strategy in range(0,5):
            execute(strategy, args)
    else:
        execute(strategy, args)

def execute(strategy, args):
    if args['all']:
        print("Solving all SUDOKUs using SAT with {} on all {}...".format(strategy,args['puzzle_filename'].name))
        solve_all(strategy,args['puzzle_filename'])
    else:
        print("Solving SUDOKU using SAT with {} on {}...".format(strategy,args['puzzle_filename'].name))
        solve_one(strategy,args['puzzle_filename'])

if __name__ == "__main__":
    main()
