
import sys
import subprocess
import os
from config import Config

class Runner:

    def __init__(self):
        self.threads = {}
        self.config = Config("C:/Users/cptli/Documents/dev/HelpfulTools/config.yaml", is_yaml=True)
        self.config.parseConfigs()

    def run_application_ui(self, program_index, user_input):
        application = self.config.applications[program_index]
        return self.start_process(application.path, [user_input])

    def run_application(self, program_index):
        application = self.config.applications[program_index]
        input_type = application.input_type
        user_input = ""
        if input_type == "file":
            user_input = input("Please enter the file: ")
        elif input_type == "string":
            user_input = input("Please enter a string: ")
        elif input_type == "number":
            user_input = input("Please enter a number: ")
        return self.start_process(application.path, [user_input])
    
    def delete_application_ui(self, program_index):
        del self.config.applications[program_index]
        self.config.updateConfig()

    def delete_application(self, program_index):
        name = self.config.applications[program_index].name
        confirm = input(f"Are you sure you want to delete {name} (yes, no): ")
        if confirm == "yes":
            del self.config.applications[program_index]
            self.config.updateConfig()

    def start_process(self, application, inputs=[]):
        args = ['python3', application]
        for input in inputs:
            args.append(input)
        self.threads[application] = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return self.threads[application]
    
    def list_applications(self):
       return self.config.applications

    def add_application_ui(self, name, file_type, path):
        self.config.addApplication(name, file_type, path)
        self.config.updateConfig()

    def add_application(self):
        name = input("Enter an application name: ")
        path = input("Enter the path to the python file: ")
        input_type = input("Enter the input_type the program users (string, file, number): ")

        print()
        print(f"Adding {name} ({path}) with input type: {input_type}")
        print()

        final = input("Enter 'yes' if this is correct: ")

        if final == 'yes':
            self.config.addApplication(name, input_type, path)
            self.config.updateConfig()

# target_file = sys.argv[1]
# inputs = sys.argv[2:]

# runner = Runner()
# # runner.start_process(target_file, inputs)
# user_input = None

# while user_input != 'q':
#     print()
#     print("Choose an option:")
#     print("l - list programs")
#     print("a - add an application")
#     print("r <selection> - run program")
#     print("d <selection> - delete program")
#     print("q - quit")

#     user_input = input("Which one?: ")

#     if user_input.startswith('l'):
#         runner.list_applications()
#     elif user_input.startswith('a'):
#         runner.add_application()
#     elif user_input.startswith('r '):
#         program_index = int(user_input.split(' ')[1])
#         runner.run_application(program_index)
#     elif user_input.startswith('d '):
#         program_index = int(user_input.split(' ')[1])
#         runner.delete_application(program_index)
#     elif user_input.startswith('q'):
#         break

# print('All done!')

# python3 .\main.py helper-packages/webp-to-png.py C:/Users/cptli/Documents/dev/HelpfulTools/helper-packages/alpha-tester.webp
# python3 .\main.py helper-packages/make-transparent.py C:/Users/cptli/Documents/dev/HelpfulTools/helper-packages/happyface.jpg