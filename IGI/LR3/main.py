from task1 import Task1
from task2 import Task2
from task3 import Task3
from task4 import Task4
from task5 import Task5

task = input("Enter the number of task, e for exit ")
print('-' * 100, sep='\n')

while True:
    if task == '1':
        Task1()
    elif task == '2':
        Task2()
    elif task == '3':
        Task3()
    elif task == '4':
        Task4()
    elif task == '5':
        Task5()
    elif task == 'e':
        break
    
    task = input("Enter the number of task, e for exit ")
    print('-' * 100, sep='\n')

print("Program ended")