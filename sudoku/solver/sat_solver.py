from ..dimacs.parse import parse_sudoku_rules,parse_sudoku_puzzles,load_dimacs_file
from ..dimacs.export import export_to_dimacs
from .heuristics import *
from ..experiment.instrumentation import start_counters,end_counters,incr_backtracks, incr_branches, save_counters
import math

# Solves all puzzles in the file with the given strategy (1,2,3)
def solve_all(strategy, puzzles_file):
    size, puzzles, _ = parse_sudoku_puzzles(puzzles_file);
    rules, symbols = parse_sudoku_rules(size)
    for puzzle in puzzles:
        formula = puzzle + rules
        export_to_dimacs(solve(strategy, formula, symbols), puzzles_file)

# Solves one SUDOKU from a DIMACS file containing both rules and puzzle
# Uses a SAT solver with a given strategy
def solve_one(strategy, dimacs_file):
    formula, symbols = load_dimacs_file(dimacs_file)
    export_to_dimacs(solve(strategy, formula, symbols), dimacs_file)

# Solves the SAT problem for the formula in CNF and the given strategy (1,2,3)
def solve(strategy, formula_str, symbols_str):
    formula, initial_model, symbols, uc = get_formula_int(formula_str, symbols_str)
    # formula = propagate_initial_model(formula, initial_model)
    start_counters(math.isqrt(len(symbols)), strategy, uc)
    result = dpll(strategy, formula, symbols, initial_model)
    end_counters()
    save_counters()
    if result is False:
        return False
    return get_result_string(result, symbols_str)

# Given an initial model assignment, it propagates the symbol values to all
# clauses in the formula
def propagate_initial_model(formula, initial_model):
    for symbol in initial_model.keys():
        formula = unit_propagation(formula, symbol if initial_model[symbol] else -symbol)
    return formula

# Converts the literals in the rules from string to int and
# forms an initial model from the puzzle unit clauses
def get_formula_int(formula_str, symbols_str):
    symbols_str = sorted(symbols_str)
    symbols_map = dict((symbols_str[i - 1], i) for i in range (1, len(symbols_str) + 1))
    symbols = set(symbols_map.values())

    uc = 0
    formula = []
    initial_model = {}
    for clause in formula_str:
        if len(clause) == 1:
            uc = uc +1
        formula.append(set(get_literal_int(literal, symbols_map) for literal in clause))
        # elif len(clause) == 1:
        #     literal = get_literal_int(clause.pop(), symbols_map)
        #     initial_model[abs(literal)] = True if literal > 0 else False
    return formula, initial_model, symbols, uc

# Converts one literal from string to int
def get_literal_int(literal, symbols_map):
    if literal.startswith('-'):
        return -symbols_map[literal.lstrip('-')]
    else:
       return symbols_map[literal]

# Converts the symbols in the truth assigment map from int to original string
def get_result_string(result, symbols):
    symbols = sorted(symbols)
    return dict((symbols[key - 1],result[key]) for key in result.keys())

# Solves the Sudoku SAT using DPLL algorithm
def dpll(strategy, formula, symbols, model):
    # print(formula, model)
    symbols, formula, model = simplify(symbols, formula, model, first_unit_clause)
    # print(formula, model)
    symbols, formula, model = simplify(symbols, formula, model, first_pure_symbol)
    # print(formula, model)
    satisfied, formula = check_if_sat(formula, model)
    # print(formula, model)
    if satisfied is False:
        incr_backtracks()
        return False
    if satisfied is True:
        return model

    # Branching based on strategy 1,2 or 3
    literal,model_1,model_2 = branch(strategy, symbols, formula, model)

    return (dpll(strategy, unit_propagation(formula, literal), symbols - {abs(literal)}, model_1) or
            dpll(strategy, unit_propagation(formula, -literal), symbols - {abs(literal)}, model_2))

# Perform given simplification of the formula iteratively until no longer possible
def simplify(symbols, formula, model, simplification_logic):
    symbol, value = simplification_logic(formula, model)
    while symbol:
        model[symbol] = value
        symbols.remove(symbol)
        formula = unit_propagation(formula, symbol if value else -symbol)
        symbol, value = simplification_logic(formula, model)
    return symbols, formula, model

#Returns the next symbol based on the branching strategy
def branch(strategy, symbols, formula, model):
    incr_branches()
    other_model = model.copy()
    literal = 0
    if strategy == 1:
        symbol, value = dlcs(formula)
    elif strategy == 2:
        symbol, value = dlis(formula)
    elif strategy == 3:
        symbol, value = jw(formula)
    elif strategy == 4:
        symbol, value = jw2(formula)
    else:
        symbol = symbols.pop()
        value = True
    symbols.discard(symbol)
    model[symbol] = value
    other_model[symbol] = not value
    literal = symbol if value else -symbol
    return literal, model, other_model

# Checks if the formula is satisfied with the given model
# The formula is satisfied if all clauses are true
# If there is at least one clause that cannot be determined, the result is None
def check_if_sat(formula, model):
    unknown_clauses = []
    for c in formula:
        val = is_clause_true(c, model)
        if val is True:
            continue
        if val is False:
            return False, unknown_clauses
        # else, if val is None
        unknown_clauses.append(c)
    if not unknown_clauses:
        return True, unknown_clauses
    return None, unknown_clauses

# Gets the symbol that forms the first remaining unit clause together
# with its truth value
def first_unit_clause(formula, model):
    bound_literals = set(model).union(set(-s for s in model))
    for clause in formula:
        unbound_literals = clause - bound_literals
        if len(unbound_literals) == 1:
            lit = unbound_literals.pop()
            return abs(lit), lit > 0
    return None, None

# (1) Removes  clause with positive (true) literal
# (2) Removes negative (false) occurences of literal from all clauses
def unit_propagation(formula, lit):
    return [clause - {-lit} for clause in formula if lit not in clause]

# Gets the first occuring pure symbol, i.e occurs only as s or -s
def first_pure_symbol(formula, model):
    unbound_literals = set().union(*formula) - set(model) - set(-s for s in model)
    positive_symbols = set(lit for lit in unbound_literals if lit > 0)
    negative_symbols = set(-lit for lit in unbound_literals if lit < 0)
    only_pos = positive_symbols - negative_symbols
    if len(only_pos) > 0:
        return only_pos.pop(), True
    only_neg = negative_symbols - positive_symbols
    if len(only_neg) > 0:
        return only_neg.pop(), True
    return None, None

# Checks if a clause resolves to true, false or unknown
def is_clause_true(clause, model):
    result = False
    for lit in clause:
        value = model.get(abs(lit))
        if value is not None:
            value = value if lit >= 0 else not value
            if value is True:
                return True
        else:
            result = None
    return result
