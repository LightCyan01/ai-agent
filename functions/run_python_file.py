import os
import subprocess
import sys

def run_python_file(working_directory, file_path):
    wd_abspath = os.path.abspath(working_directory)
    
    if file_path:
        target_file = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not target_file.startswith(wd_abspath):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_file):
        return f'Error: File "{file_path}" not found.'
    
    if not target_file.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        run = subprocess.run([sys.executable, target_file], cwd=wd_abspath, timeout=30, capture_output=True, text=True, check=True)
        
        if not run.stdout and not run.stderr:
            return "No output produced"
        
        return f"STDOUT: {run.stdout}\nSTDERR: {run.stderr}"
    
    except subprocess.CalledProcessError as e:
        return f"Process exited with code {e.returncode}"
    except Exception as e:
        return f"Error: executing Python file: {e}"
    