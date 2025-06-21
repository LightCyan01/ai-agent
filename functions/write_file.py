import os

def write_file(working_directory, file_path, content):
    wd_abspath = os.path.abspath(working_directory)
    
    if file_path:
        target_file = os.path.abspath(os.path.join(wd_abspath, file_path))
    
    if not target_file.startswith(wd_abspath):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(target_file):
        try:
            if not os.path.dirname(target_file):
                os.makedirs(os.path.dirname(target_file))
        except Exception as e:
            return f'Error: {e}'
    
    with open(target_file, "w") as f:
        f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'