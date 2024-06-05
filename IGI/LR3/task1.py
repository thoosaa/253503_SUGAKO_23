'''
Task 1.23. Program to calculate the value of a function using a power series expansion with a given accuracy eps. 
The maximum number of iterations is 500. Output the number of terms of the series for the specified accuracy. 
Present the result in the form of a table.

Lab: 3
Version: 1.0
Dev: Sugako Tatyana
Date: 24.03.2024
'''

import math
from prettytable import PrettyTable 
from inputCheck import getFloatNumber

def MathF(x):
    """Calculate e ** x"""
    return math.log(1 + x)

def F(x, eps):
    """Calculate e ** x using Taylor series"""
    td = []
    n = 0
    res = 0
    while(abs(MathF(x) - res) > eps):
        if n <= 500:
            n += 1
            res += (-1) ** (n - 1) * x ** n / n
        else:
            break
    td.extend([round(x, 3), n, MathF(x), res, eps])
    return td

def PrintTable(td):
    """Print table"""
    th = ['x', 'n', 'F(x)', 'Math F(x)', 'eps']
    columns = len(th)
    table = PrettyTable(th)
    while td:
        table.add_row(td[:columns])
        td = td[columns:]
    print(table)


def Task1():
    """Calculate the number of terms of the series for the specified accuracy. Result is a table."""
    print("Task 1", '-' * 100, sep='\n')
    x, eps = getFloatNumber("Enter x: "), getFloatNumber("Enter eps: ")
    PrintTable(F(x, eps))
    print('-' * 100)
