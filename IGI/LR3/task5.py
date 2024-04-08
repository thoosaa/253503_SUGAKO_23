'''
Task 5.23. In a list consisting of integer elements, calculate the number of odd negative elements 
and the sum of the list elements up to the last element equal to zero

Lab: 3
Version: 1.0
Dev: Sugako Tatyana
Date: 24.03.2024
'''

from listInit import ListInit, ListGenInit
from inputCheck import getNumber

def listItems(lst):
    """Create generator object"""
    for items in lst:
        yield items

def PrintList(lst):
    """Print list using generator"""
    gen = listItems(lst)
    n = 0

    while n < len(lst):
        print(next(gen), end=' ')
        n += 1

def CountOddNegative(lst):
    """Calculate the number of odd negative elements"""
    res = 0
    for item in lst:
        if item < 0 and item % 2:
            res += 1
    return res

def SumUntilZero(lst):
    """Calculate the sum of the list elements up to the last element equal to zero"""
    sum = 0
    for item in lst:
        if item != 0:
            sum += item
        else:
            break
    return sum

def Task5():
    print("Task 5", '-' * 100, sep='\n')
    choice = input("Enter g for generator, anything else for self-input:")
    if choice == "g":
        lst = list(ListGenInit(int(input("Enter the number of el in list: "))))
    else:
        lst = ListInit(int(input("Enter the number of elements in list: ", end='\n')))
    PrintList(lst)
    print(f"Number of odd negative elements: {CountOddNegative(lst)}", f"Sum of elements up to zero: {SumUntilZero(lst)}" ,sep='\n')
    print('-' * 100)