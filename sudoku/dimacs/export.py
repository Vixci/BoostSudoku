def export_to_dimacs(truth_assigmnent, filename):
    #result = "c Sudoku puzzle solution\n"
    #result = result + "p cnf {} {} 0\n".format(len(truth_assigmnent), len(truth_assigmnent))
    # TODO: should all sudoku solutions be in the same file?
    result = ""
    for key in sorted(truth_assigmnent.keys()):
        # TODO: Should it output for true assigments only or also for false ones?
        result = result + key + "  " if truth_assigmnent[key] else result
    result = result + "\n"
    fileparts = filename.split('.')
    filename = fileparts[0] + ".out"
    f = open(filename, 'a')
    f.write(result)
    f.close()

def write_dimacs_files(puzzles, rules):
    for i in range(len(puzzles)):
        f = open("input/sudokus/sudoku{}.txt".format(i), 'w')
        f.write(rules)
        f.write(puzzles[i])
        f.close()
