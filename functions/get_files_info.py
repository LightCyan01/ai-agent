import os

MAX_CHARS = 10000

def get_files_info(working_directory, directory=None):
    wd_abspath = os.path.abspath(working_directory)
    
    if directory:
        target_dir = os.path.abspath(os.path.join(working_directory, directory))
    else:
        target_dir = wd_abspath
        
    if not target_dir.startswith(wd_abspath):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    
    file_list = []
    for file in os.listdir(target_dir):
        file_path = os.path.join(target_dir, file)
        size = os.path.getsize(file_path)
        is_dir = os.path.isdir(file_path)
        file_list.append(f"- {file}: file_size={size} bytes, is_dir={is_dir}")
    return "\n".join(file_list)
    

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