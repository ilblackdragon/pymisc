import math
import itertools

def euclidian_distance(l1, l2):
    """
    Euclidian distance
    >>> euclidian_distance([1, 2], [2, 1])
    1.4142135623730951
    """
    dist = 0
    for x1, x2 in itertools.izip(l1, l2):
        dist += (x1 - x2) ** 2
    return math.sqrt(dist)

def hamming_distance(s1, s2):
    """
    http://en.wikipedia.org/wiki/Hamming_distance
    >>> hamming_distance("toned", "roses")
    3
    """
    count = 0
    for c1, c2 in itertools.izip(s1, s2):
         if c1 != c2:
             count += 1
    return count

def levenshtein_distance(seq1, seq2): 
    """
    http://en.wikipedia.org/wiki/Levenshtein_distance    
    >>> levenshtein_distance("HURQBOHP", "QKHOZ")
    7
    >>> levenshtein_distance('AATZ', 'AAAZ')
    1
    >>> levenshtein_distance('AATZZZ', 'AAAZ')
    3
    """
    oneago = None
    thisrow = range(1, len(seq2) + 1) + [0]
    for x in xrange(len(seq1)):
        oneago, thisrow = thisrow, [0] * len(seq2) + [x + 1]
        for y in xrange(len(seq2)):
            delcost = oneago[y] + 1
            addcost = thisrow[y - 1] + 1
            subcost = oneago[y - 1] + (seq1[x] != seq2[y])
            thisrow[y] = min(delcost, addcost, subcost)
    return thisrow[len(seq2) - 1]
    
def damerau_levenshtein_distance(seq1, seq2):
    """
    http://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance
    >>> damerau_levenshtein_distance("HURQBOHP", "QKHOZ")
    6
    """
    oneago = None
    thisrow = range(1, len(seq2) + 1) + [0]
    for x in xrange(len(seq1)):
        twoago, oneago, thisrow = oneago, thisrow, [0] * len(seq2) + [x + 1]
        for y in xrange(len(seq2)):
            delcost = oneago[y] + 1
            addcost = thisrow[y - 1] + 1
            subcost = oneago[y - 1] + (seq1[x] != seq2[y])
            thisrow[y] = min(delcost, addcost, subcost)
            if (x > 0 and y > 0 and seq1[x] == seq2[y - 1]
                and seq1[x-1] == seq2[y] and seq1[x] != seq2[y]):
                thisrow[y] = min(thisrow[y], twoago[y - 2] + 1)
    return thisrow[len(seq2) - 1]