
def sort_by_indices(data):
    """
    This function sorts data and return permuted indices
    >>> sort_by_indices([1, 3, 0, 9, 5])
    [2, 0, 1, 4, 3]
    """
    return sorted(range(len(data)), key = data.__getitem__)

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
