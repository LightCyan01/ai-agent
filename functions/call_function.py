from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file
from google.genai import types

import os


def call_function(function_call_part, verbose=False):
    fc_name = function_call_part.name
    fc_args = function_call_part.args
    wd_abspath = os.path.abspath("./calculator")
    fc_args["working_directory"] = wd_abspath
    
    if verbose:
        print(f"Calling function: {fc_name}({fc_args})")
    else:
        print(f" - Calling function: {fc_name}")
        
    if fc_name == "get_files_info":
        result = get_files_info(**fc_args)
    elif fc_name == "get_file_content":
        result = get_file_content(**fc_args)
    elif fc_name == "write_file":
        result = write_file(**fc_args)
    elif fc_name == "run_python_file":
        result = run_python_file(**fc_args)
    else:
        return types.Content(
            role="tool",
            parts=[
            types.Part.from_function_response(
            name=fc_name,
            response={"error": f"Unknown function: {fc_name}"},
        )
    ],
)
    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=fc_name,
            response={"result": result},
        )
    ],
)
    