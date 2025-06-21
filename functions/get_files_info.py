import os

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