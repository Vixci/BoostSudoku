import math
from itertools import chain
from collections import Counter

def dlcs(formula):
    occ = {}
    for lit in chain(*formula):
        occ[lit] = occ.get(lit, 0) + 1
    #find max
    max = 0
    maxKey = None
    for key in occ.keys():
        absKey = abs(key)
        val = occ.get(absKey, 0) + occ.get(-absKey, 0)
        if val > max:
            max = val
            maxKey = absKey
    if maxKey is None:
        return None
    return maxKey if occ.get(maxKey, 0) >= occ.get(-maxKey, 0) else -maxKey

def dlis(formula):
    occ = {}
    for lit in chain(*formula):
        occ[lit] = occ.get(lit, 0) + 1
    if bool(occ):
        return max(occ, key = occ.get)
    return None

def jw(formula):
    occ = {}
    for c in formula:
        for i in c:
            occ[i] = occ.get(i, 0) + math.pow(2, -len(c))
    if bool(occ):
        return max(occ, key = occ.get)
    return None

def jw2(formula):
    occ = {}
    for c in formula:
        for i in c:
            occ[i] = occ.get(i, 0) + math.pow(2, -len(c))
    #find max
    max = 0
    maxKey = None
    for key in occ.keys():
        absKey = abs(key)
        val = occ.get(absKey, 0) + occ.get(-absKey, 0)
        if val > max:
            max = val
            maxKey = absKey
    if maxKey is None:
        return None
    return maxKey if occ.get(maxKey, 0) >= occ.get(-maxKey, 0) else -maxKey
