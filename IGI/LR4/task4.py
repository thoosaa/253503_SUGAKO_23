'''
Task 4.23. Construct a rhombus by side a and obtuse angle R (in degrees).

Lab: 4
Version: 1.0
Dev: Sugako Tatyana
Date: 20.04.2024
'''
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from abstraction import GeometricFigure

import matplotlib.pyplot as plt
import numpy as np

from validation import int_input

class FigureColor:
    COLORS = {
        "w": "white",
        "b": "blue",
        "y": "yellow",
        "p": "pink"
    }
    
    def __init__(self, color: str=None):
        self.__color = color

    @property
    def color(self):
        return self.__color
    
    @color.setter
    def color(self, color):    
        self.__color = color

class Rhombus:
    FIGURE_NAME = "Rhombus"

    def __init__(self, side_length, obtuse_angle, text):
        self.side_length = side_length
        self.obtuse_angle = obtuse_angle
        self.text = text
        self.obj_color = FigureColor('b')
    
    @classmethod
    def get_figure_name(cls):
        return f"{cls.FIGURE_NAME}" 

    @property
    def obtuse_angle(self):
        return self.__obtuse_angle
    
    @obtuse_angle.setter
    def obtuse_angle(self, obtuse_angle):
        self.__obtuse_angle = obtuse_angle

    @property
    def text(self):
        return self.__text
    
    @text.setter
    def text(self, text):
        self.__text = text

    @property
    def side_length(self):
        return self.__side_length
    
    @side_length.setter
    def side_length(self, side_length):
        self.__side_length = side_length
    
    def area(self):
        return f"Area: {self.side_length**2* np.sin(np.deg2rad(180 - self.obtuse_angle))}"
    
    def __str__(self):
        return f"Figure name: {self.get_figure_name()}\nside: {self.side_length}\nangle: {self.obtuse_angle}"

    def plot_rhombus(self):
        fig, ax = plt.subplots()

        angle_rad = np.radians(self.obtuse_angle) 
        x = [0, self.side_length * np.cos(angle_rad), 0, -self.side_length * np.cos(angle_rad), 0]
        y = [0, self.side_length * np.sin(angle_rad), 2 * self.side_length * np.sin(angle_rad), self.side_length * np.sin(angle_rad), 0]

        ax.plot(x, y, color=self.obj_color.color)
        # ax.set_aspect('equal', adjustable='box')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title(self.text)

        plt.grid(True)
        plt.show()


def Task4():
    form = Rhombus(int_input("enter side: "), int_input("enter angle: "), input('Enter text: '))

    while True:
        way = int_input("Choose:\n1. Calculate rhombus's area\n2. Plot rhombus\n3. Output class data\n4. Change side length\n5. Change obtuse angle\n6. Change figure color\n7. Change text\n8. Exit")
        match way:
            case 1:
                print(form.area())
            case 2:
                form.plot_rhombus()
            case 3:
                print(form)
            case 4:
                form.side_length = int_input('Enter side length: ')
            case 5:
                form.obtuse_angle = int_input("Enter angle: ")
            case 6: 
                color_choice = input(f"Change color: {FigureColor.COLORS.keys()}")
                if color_choice in FigureColor.COLORS:
                    form.obj_color.color = FigureColor.COLORS[color_choice]
                else:
                    print("Invalid color choice.")
            case 7:
                text = input('Enter text')
                form.text = text
            case 8:
                break
            case _:
                continue
