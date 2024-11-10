
import os
import importlib.util
from pathlib import Path
import signal
import sys
import subprocess
import threading
import os
from multiprocessing import Process

class Runner():

    def __init__(self, directory):
        self.directory = directory
        self.threads = {}
        self.check_for_complete_threads()

    @classmethod
    def initialize(cls, directory):
        return cls(directory)
    
    def check_for_complete_threads(self):
        def check_threads():
            markedForDeletion = []
            for key in self.threads:
                isAlive = self.threads[key].poll()
                if isAlive is not None:
                    markedForDeletion.append(key)
            for key in markedForDeletion:
                del self.threads[key]
            self.timer = threading.Timer(1, check_threads)
            self.timer.start()
        self.timer = threading.Timer(1, check_threads)
        self.timer.start()

    def list_python_files(self):
        """List all Python files in the specified directory."""
        python_files = []
        for root, dirs, files in os.walk(self.directory):
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))
        return python_files

    def import_python_file_as_module(self, file_path):
        """Dynamically import a Python file as a module."""
        module_name = os.path.basename(file_path).replace('.py', '')
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module

    def run_scripts_in_directory(self):
        """Import and run all Python scripts in the specified directory."""
        python_files = self.list_python_files(self.directory)
        for file_path in python_files:
            module = self.import_python_file_as_module(file_path)
            # run_module_function(module)
    
    def start_process(self, filename, inputs):
        args = ["python3", filename]
        for input in inputs:
            args.append(input)
        return subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    def run_file(self, file, inputs):
        p = self.start_process(file, inputs)
        self.threads[file] = p

    def list_processes(self):
        keys = list(self.threads.keys())
        processes = []
        for key in keys:
            processes.append(f"1 - {key}")
        return processes

    def kill_process(self, target):
        process = self.threads[target]
        process.kill()
        del self.threads[target]

    def run(self):
        print(self.list_python_files(self.directory))

    def end(self):
        self.timer.cancel()
    
    @staticmethod
    def commands():
        print("What would you like to do?")
        print("l - list programs")
        print("ls - list threads")
        print("s <name> - start a program with the provided name")
        print("k <name> - kill the program with the provided name")
        print("q - quit the program")

if __name__ == "__main__":
    directory = "helper-packages/" #input("Enter the directory path containing Python scripts: ")
    runner = Runner.initialize(directory=directory)

    def signal_handler(sig, frame):
        runner.end()
        print("Bye <3")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    Runner.commands()
    user_input = input("Command: ")
    while user_input != "q":
        if user_input == "l":
            print("Files:")
            files = runner.list_python_files()
            for file in files:
                print(file)
        elif user_input == "ls":
            print("Processes: ")
            processes = runner.list_processes()
            for process in processes:
                print(process)
        elif user_input.startswith("s"):
            file_target = user_input.split(" ")[1]
            inputs = user_input.split(" ")[2::]
            files = runner.list_python_files()
            for file in files:
                if file_target in file:
                    runner.run_file(file, inputs)
                    break
        elif user_input.startswith("k"):
            file_target = user_input.split(" ")[1]
            processes = runner.list_processes()
            print("Processes are:")
            for process in processes:
                print(process)
                if file_target in process:
                    print(f"Killing {process}")
                    runner.kill_process(process)
                    break
        elif user_input == "q":
            print("Runner exiting.")
            break
        print(" ")
        Runner.commands()
        user_input = input("Command: ")
    signal_handler(None, None)
