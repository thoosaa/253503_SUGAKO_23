def isDigit(s):
    if s.startswith("-"):
        s = s[1:]
    return s.isdigit()

def getNumber():
    while True:
        num = input("Enter number: ") 
        if isDigit(num) : 
            return int(num)


def getFloatNumber(inputStr):
    while True:
        num = input(inputStr)
        try:                                 
            temp_num = float(num)
        except ValueError:                   
            print('Not a number')
        else: 
            break
    return float(num)