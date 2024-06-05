from inputCheck import getNumber

def ListInit(n):
    """Create list with user input"""
    lst = []
    for _ in range(0, n): 
        lst.append(getNumber())
    # print(lst)
    return lst

def ListGenInit(n):
    current = 0
    while current <= n:
        yield current
        current += 1