'''
Task 1.23. Information is collected about the students who entered the university: surname, whether they need dormitory, work experience (if any),
what they graduated from, what language they studied. 
Determine: 
a) how many people need dormitory; 
b) lists of students with more than 2 years of work experience; 
c) lists of students who graduated from the technical school; 
d) lists of language groups. Output the information about the student entered from the keyboard

Lab: 4
Version: 1.0
Dev: Sugako Tatyana
Date: 20.04.2024
'''

import csv
import pickle
from validation import int_input

class StudentDatabase:
    def __init__(self):
        self.students = {}

    def add_student(self, student):
        """
        Add student to Database
        """
        self.students[student["surname"]] = {
            'needs_dormitory': student["needs_dormitory"],
            'work_experience': student["work_experience"],
            'graduation_place': student["graduation_place"],
            'language_studied': student["language_studied"]
        }

    def count_students_needing_dormitory(self):
        """
        Get student in need of dorm
        """
        count = sum(student['needs_dormitory'] for student in self.students.values())
        return count

    def students_with_experience_over_2_years(self):
        """
        Get students over 2 years of experience
        """
        return [surname for surname, info in self.students.items() if int(info["work_experience"]) > 2]



    def students_graduated_from_technical_college(self):
        """
        Get graduates from technicum
        """
        return [surname for surname, info in self.students.items() if "graduation_place" in info and "technicum" in info["graduation_place"].lower()]

    def language_groups(self):
        """
        Get language groups
        """
        language_groups_dict = {}
        for surname, info in self.students.items():
            language = info['language_studied']
            if language not in language_groups_dict:
                language_groups_dict[language] = [surname]
            else:
                language_groups_dict[language].append(surname)
        return language_groups_dict

    def get_student_info(self, surname):
        return self.students.get(surname)

    def input_student_details(self):
        """
        Function to input student details from user and add them to the database
        """
        surname = input("Enter student's surname: ")
        needs_dormitory = input("Does the student need a dormitory? (Yes/No): ").lower() == "yes"
        work_experience = input("Enter work experience (if any write 0) ")
        graduation_place = input("What did the student graduate from? ")
        language_studied = input("What language did the student study? ")
        
        self.add_student({
            "surname": surname,
            "needs_dormitory": needs_dormitory,
            "work_experience": work_experience,
            "graduation_place": graduation_place,
            "language_studied": language_studied
        })


class CSVSerializer(StudentDatabase):
    def __init__(self):
        super().__init__()

    def serialize(self):
        with open("students.csv", "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['surname', 'needs_dormitory', 'work_experience', 'graduation_place', 'language_studied'])
            for surname, info in self.students.items():
                writer.writerow([surname, info['needs_dormitory'], info['work_experience'], info['graduation_place'], info['language_studied']])
    
    def deserialize(self):
        with open("students.csv", newline='') as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header row
            for row in reader:
                surname, needs_dormitory, work_experience, graduation_field, language_studied = row
                self.add_student({
                    "surname": surname,
                    "needs_dormitory": needs_dormitory.lower() == "true",
                    "work_experience": work_experience,
                    "graduation_field": graduation_field,
                    "language_studied": language_studied
                })
    
    def __str__(self):
        return str(self.students)
    

class PickleSerializer(StudentDatabase):
    def __init__(self):
        super().__init__()

    def serialize(self):
        with open("students.pkl", "wb") as file:
            pickle.dump(self.students, file)

    def deserialize(self):
        with open("students.pkl", 'rb') as file:
            data = pickle.load(file)
        print(data)
        self.students = data

    def __str__(self):
        return str(self.students)



def Task1():
    file_handler = int_input("Choose file handler:\n1. CSV\n2. Pickle ")
    serializer = CSVSerializer() if file_handler == 1 else PickleSerializer()
    
    while True:
        way = int_input("Choose: \n1. Add student\n2. Write in file\n3. Inspect file data\n4. StudentDB functions\n5. Exit\n")

        match way:
            case 1:
                serializer.input_student_details()
            case 2:
                serializer.serialize()
            case 3: 
                serializer.deserialize()
            case 4:
                # a) Count of students needing dormitory
                print("Number of students needing dormitory:", serializer.count_students_needing_dormitory())

                # b) Students with work experience over 2 years
                print("Students with work experience over 2 years:", serializer.students_with_experience_over_2_years())

                # c) Students graduated from technical college
                print("Students graduated from technical college:", serializer.students_graduated_from_technical_college())

                # d) Language groups
                print("Language groups:", serializer.language_groups())
            case 5:
                break
            case _:
                continue