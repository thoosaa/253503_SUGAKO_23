def int_input(prompt):
    while True:
        try:
            num = int(input(prompt))
            return num  # Возвращаем введенное целое число
        except ValueError:
            print("Invalid input. Please enter an integer.")
