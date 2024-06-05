'''
Task 3.23. Determine if the string entered from the keyboard is a hexadecimal number

Lab: 3
Version: 1.0
Dev: Sugako Tatyana
Date: 24.03.2024
'''

def GetHexSym():
    """Get all correct symbols for hex numbers"""
    correctSym = [ ]
    correctSym.extend([str(i) for i in range(0, 10)])
    correctSym.extend([chr(65 + i) for i in range(0, 6)])
    correctSym.extend([chr(97 + i) for i in range(0, 6)])
    return correctSym

def CheckHex(str):
    """Check if string is hex"""
    hex_sym = GetHexSym()
    # print(hex_sym, *str)
    for sym in str:
        if sym not in hex_sym:
            print("Not a hex number")
            break
    else:
        print("Hex number")

def divider_decorator(func):
    def wrapper():
        print("Task 3", '-' * 100, sep='\n')
        func()
        print('-' * 100)
    return wrapper

@divider_decorator
def Task3():
    """Determine if the string entered from the keyboard is a hexadecimal number"""
    CheckHex(input("Enter string: "))
