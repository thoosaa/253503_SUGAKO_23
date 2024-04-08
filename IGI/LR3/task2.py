'''
Task 2.23. Organize a loop that accepts integers and finds the number of numbers greater than 23. End with input 15

Lab: 3
Version: 1.0
Dev: Sugako Tatyana
Date: 24.03.2024
'''
from inputCheck import getNumber

def Task2():
    print("Task 2", '-' * 100, sep='\n')
    """Find the number of numbers greater than 23. End with input 15"""
    greater23 = 0
    num = getNumber()
    while(num != 15):
        if(num > 23):
            greater23 += 1
        num = getNumber()
    print(f"Number of integers greater than 23: {greater23}")
    print('-' * 100)