from functions.run_python_file import run_python_file

print("result for main.py")
print(run_python_file("calculator", "main.py"))

print("\nresults for tests.py")
print(run_python_file("calculator", "tests.py"))

print("\nresults for main.py (error)")
print(run_python_file("calculator", "../main.py"))

print("\nresults for nonexistent")
print(run_python_file("calculator", "nonexistent.py"))