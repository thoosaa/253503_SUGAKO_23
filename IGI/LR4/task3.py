'''
Task 3.23. In accordance with the task of their variant to refine the program from LR3, using the class and provide:
a) determination of additional parameters arithmetic mean of sequence elements, median, mode, variance, standart deviation of the sequence;
b) using the matplotlib library to draw graphs of different colors in one coordinate axis:
⦁ graph according to the obtained data of the function decomposition into a series presented in the table, 
⦁ the graph of the corresponding function represented with the help of the math module. Provide display of coordinate axes, legend, text and annotation.
c) save the graphs to a file

Lab: 4
Version: 1.0
Dev: Sugako Tatyana
Date: 20.04.2024
'''

import math
import statistics
import matplotlib.pyplot as plt
from validation import int_input

class LogCalculate:
    def mathF(self, x):
        return math.log(1 + x)
    
    def F(self, x, eps):
        n = 0
        res = 0
        seq = []
        while(abs(self.mathF(x) - res) > eps):
            if n <= 500:
                n += 1
                res += (-1) ** (n - 1) * x ** n / n
                seq.append((-1) ** (n - 1) * x ** n / n)
            else:
                break
        return [res, seq]
    
    def statisticParametrs(self, seq):
        try:
            print(f"Mean {statistics.mean(seq)}\n Median {statistics.median(seq)}\n Mode {statistics.mode(seq)}\nVariance {statistics.variance(seq)}\nStandart deviation {statistics.stdev(seq)}")
        except statistics.StatisticsError as e:
            print("Error:", e)

    def plotGraphics(self, eps):
        y1 = [self.F(i / 10, eps)[0] for i in range(0, 10)]
        y2 = [self.mathF(i / 10) for i in range(0, 10)]
        plt.plot(y1, 'bo-', label='Custom log(1 + x)')
        plt.plot(y2, 'ro-', label='Math log(1 + x)')
        plt.legend()
        plt.savefig('log.jpg')
        plt.show()

def Task3():
    calc = LogCalculate()

    while True:
        way = int_input("Choose: \n1. Calculate statistics parametrs\n2. Plot graph\n3.Exit\n")

        match way:
            case 1:
                x, eps = float(input("Enter x: ")), float(input("Enter eps: "))
                seq = calc.F(x, eps)[1]
                calc.statisticParametrs(seq)
            case 2:
                eps = float(input("Enter eps: "))
                calc.plotGraphics(eps)  
            case 3:
                break
            case _:
                continue
