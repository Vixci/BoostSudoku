import math

def dlcs(formula):
    occ = {}
    for c in formula:
        for i in c:
            if abs(i) in occ:
                if i > 0:
                    occ[abs(i)] = (occ[abs(i)][0] + 1, occ[abs(i)][1])
                else:
                    occ[abs(i)] = (occ[abs(i)][0], occ[abs(i)][1] + 1)
            else:
                occ[abs(i)] = (1,0) if i > 0 else (0,1)
    #find max
    max = 0
    maxKey = 0
    for key in occ.keys():
        val = occ[key][0] + occ[key][1]
        if val > max:
            max = val
            maxKey = key

    if occ[maxKey][0] >= occ[maxKey][1]:
        return maxKey, True
    else:
        return maxKey, False

def dlis(formula):
    occ = {}
    for c in formula:
        for i in c:
            if abs(i) in occ:
                if i > 0:
                    occ[abs(i)] = (occ[abs(i)][0] + 1, occ[abs(i)][1])
                else:
                    occ[abs(i)] = (occ[abs(i)][0], occ[abs(i)][1] + 1)
            else:
                occ[abs(i)] = (1,0) if i > 0 else (0,1)
    #find max
    max = 0
    maxKey = 0
    maxPon = 0
    for key in occ.keys():
        val = 0
        pon = 0
        if occ[key][0] > occ[key][1]:
            val = occ[key][0]
            pon = True
        else:
            val = occ[key][1]
            pon = False
        if val > max:
            max = val
            maxKey = key
            maxPon = pon

    return maxKey, maxPon

def jw(formula):
    occ = {}
    for c in formula:
        for i in c:
            if i in occ:
                occ[i] += math.pow(2, -len(c))
            else:
                occ[i] = math.pow(2, -len(c))

    max = 0
    maxKey = 0

    for key in occ.keys():
        if occ[key] > max:
            max = occ[key]
            maxKey = key

    pon = True if maxKey > 0 else False

    return maxKey, pon

def jw2(formula):
    occ = {}
    for c in formula:
        for i in c:
            if abs(i) in occ:
                if i > 0:
                    occ[abs(i)] = (occ[abs(i)][0] + math.pow(2, -len(c)), occ[abs(i)][1])
                else:
                    occ[abs(i)] = (occ[abs(i)][0], occ[abs(i)][1] + math.pow(2, -len(c)))
            else:
                occ[abs(i)] = (math.pow(2, -len(c)),0) if i > 0 else (0,math.pow(2, -len(c)))

    #find max
    max = 0
    maxKey = 0
    maxPon = 0
    for key in occ.keys():
        val = 0
        pon = 0
        if occ[key][0] > occ[key][1]:
            val = occ[key][0]
            pon = True
        else:
            val = occ[key][1]
            pon = False
        if val > max:
            max = val
            maxKey = key
            maxPon = pon

    return maxKey, maxPon
