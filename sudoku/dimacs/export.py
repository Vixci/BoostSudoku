import os

def initialize_export_file(input_filename):
    fileparts = input_filename[::-1].split('.', 1)
    filename = fileparts[1][::-1] + ".out"
    if os.path.exists(filename):
        os.remove(filename)
    return filename

def export_to_dimacs(truth_assigmnent, filename):
    #result = "c Sudoku puzzle solution\n"
    #result = result + "p cnf {} {} 0\n".format(len(truth_assigmnent), len(truth_assigmnent))
    # TODO: should all sudoku solutions be in the same file?
    result = ""
    if truth_assigmnent is not False:
        for key in sorted(truth_assigmnent.keys()):
            # TODO: Should it output for true assigments only or also for false ones?
            result = result + key + "  " if truth_assigmnent[key] else result
    result = result + "\n"

    f = open(filename, 'a')
    f.write(result)
    f.close()

def write_dimacs_files(puzzles, rules, puzzle_size):
    for i in range(len(puzzles)):
        f = open("data/sudokus/sudoku{}-{}.txt".format(puzzle_size, i), 'w')
        f.write(rules)
        f.write(puzzles[i])
        f.close()
