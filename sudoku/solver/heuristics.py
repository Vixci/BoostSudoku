 import math

def jw(cnf, value=2):   # One sided Jeroslow-Wang
    select = {}
    for clause in cnf:
        for literal in clause:
            if literal in select:
                select[literal] += math.pow(value, -len(clause))    # formula ∑ 2 ^ -|ω|
            else:
                select[literal] = math.pow(value, -len(clause))
    return max(select, key=select.get)


def jw2(cnf, value=2):   # Two sided Jeroslow-Wang
    select = {}
    for clause in cnf:
        for literal in clause:
            literal = abs(literal)  # Combine
            if literal in select:
                select[literal] += math.pow(value, -len(clause))
            else:
                select[literal] = math.pow(value, -len(clause))
    return max(select, key=select.get)
