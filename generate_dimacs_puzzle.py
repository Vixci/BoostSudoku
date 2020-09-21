import argparse
from sudoku.dimacs.parse import get_dimacs_strings_from_file
from sudoku.dimacs.export import write_dimacs_files

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-n","--number", type=int, choices=range(1,1000), default=1, help="Number of rows to process in separate files")
    ap.add_argument("puzzle_filename", type=argparse.FileType('r'), help= "If present, solves all the puzzles expressed in dot format present in the file and infers the rules from the size of the rows")
    args = vars(ap.parse_args())

    print("Generating {} DIMACS files from {}".format(args['number'],args['puzzle_filename'].name))

    puzzles, rules = get_dimacs_strings_from_file(args['number'],args['puzzle_filename'])
    write_dimacs_files(puzzles, rules)

if __name__ == "__main__":
    main()
