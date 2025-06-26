import json

class Counter:
    def __init__(self,P = 0, F = 0):
        self.__P = P
        self.__F = F
    def count_Pass(self):
        self.__P += 1
    def count_fail(self):
        self.__F += 1
    def showPass(self):
        print("Pass Students : ", self.__P)
    def showFail(self):
        return self.__F


def display_student_summary(file_path):
    counter = Counter()
    """
    Reads student data from a JSON file and displays S.N., Student Name, Status, and SGPA.

    Args:
        file_path (str): The path to the JSON file containing student results.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            students_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found. Please ensure 'pu_results.json' is in the same directory.")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{file_path}'. Check if it's a valid JSON file.")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return

    
    print("S.N. | Student Name             | Status | SGPA")
    print("-----|--------------------------|--------|-------")

    for i, student in enumerate(students_data):
        # Using .get() for safe access in case a key is missing
        student_name = student.get('name', 'N/A')
        status = student.get('status', 'N/A')
        sgpa = student.get('sgpa', 'N/A')

        if status.lower() == "pass":
            counter.count_Pass()
        elif status.lower() == "fail":
            counter.count_fail()

        # Ensure name fits in a fixed-width column, truncate if too long
        display_name = (student_name[:24] + '..') if len(student_name) > 26 else student_name
        
        # Print formatted output
        print(f"{i+1:<4} | {display_name:<24} | {status:<6}  | {sgpa:<5}")
    
    counter.showPass()
    print("Fail Student : ", counter.showFail())

# Specify the path to your uploaded JSON file
file_name = "Result\pu_results.json"

# Call the function to display the summary
display_student_summary(file_name)

# print("No of Pass Student = ", {P})
# print("No of Fail Student = ", {F})