import os

MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    wd_abspath = os.path.abspath(working_directory)
    
    if file_path:
        target_file = os.path.abspath(os.path.join(wd_abspath, file_path))
    
    if not target_file.startswith(wd_abspath):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    with open(target_file, "r") as f:
        content = f.read()
        
        if len(content) > MAX_CHARS:
            trunc = content[:MAX_CHARS] + f'[...File "{target_file}" truncated at 10000 characters]'
            return trunc
        
        return content