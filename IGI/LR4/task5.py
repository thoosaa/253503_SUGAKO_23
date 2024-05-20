'''
Task 5.23. Construct a rhombus by side a and obtuse angle R (in degrees).

Lab: 4
Version: 1.0
Dev: Sugako Tatyana
Date: 20.04.2024
'''

import numpy as np

class MatrixHandler:
    def __init__(self, matrix):
        self.matrix = matrix

    def sort_by_last_column(self):
        sorted_matrix = self.matrix[self.matrix[:, -1].argsort()[::-1]]
        return sorted_matrix

    @staticmethod
    def mean_last_column(self):
        mean_standard = np.mean(self.matrix[:, -1])

        mean_formula = np.sum(self.matrix[:, -1]) / self.matrix.shape[0]

        return round(mean_standard, 2), round(mean_formula, 2)

def Task5():
    matrix = np.array([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ])

    handler = MatrixHandler(matrix)

    while True:
        way = int(input("Choose:\n1. Sort matrix by last column\n2. Calculate mean of last column\n3. Exit\n"))
        if way == 1:
            sorted_matrix = handler.sort_by_last_column()
            print("Sorted Matrix:")
            print(sorted_matrix)
        elif way == 2:
            mean_standard, mean_formula = handler.mean_last_column()
            print("\nMean value of last column:")
            print("Using standard function:", mean_standard)
            print("Using formula:", mean_formula)
        elif way == 3:
            break
        else:
            print("Invalid choice. Please choose again.")