from task1 import Task1
from task2 import Task2
from task3 import Task3
from task4 import Task4
from task5 import Task5
from validation import int_input

while True:
        way = int_input("Choose: \n1. Task 1 \n2. Task 2\n3. Task 3\n4. Task 4\n5. Task 5\n6. Exit")
        match way:
            case 1:
                Task1()
            case 2:
                Task2()
            case 3:
                Task3()
            case 4:
                Task4()
            case 5:
                Task5()
            case 6:
                break
            case _:
                continue