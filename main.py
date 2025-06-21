import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv
from functions.call_function import call_function

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    
    if len(sys.argv) < 2:
        raise Exception("Text contents needed")
    
    user_prompt = sys.argv[1]
    flag_verbose = False
    
    if len(sys.argv) >= 3:
        arg = sys.argv[2]
        if arg.startswith("--"):
            command = arg[2:]
            
            match command:
                case "verbose":
                    flag_verbose = True
                case _:
                    raise Exception("Unknwon flag")
    
    schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
    
    schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the contents of the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory.",
            ),
        },
    ),
)
    
    schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites the contents of the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written to the specified file.",
            )
        },
    ),
)
    
    schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python prgram",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python program to run, relative to the working directory.",
            ),
        },
    ),
)
    
    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ]
)
    
    messages = [types.Content(role="User", parts=[types.Part(text=user_prompt)])]
    response = client.models.generate_content(model='gemini-2.0-flash-001', 
                                              contents=messages,
                                              config=types.GenerateContentConfig(
                                                  tools=[available_functions],
                                                  system_instruction=system_prompt,))
    
    
    if response.function_calls:
        for fc in response.function_calls:
            fc_result = call_function(fc, flag_verbose)
            
            part = fc_result.parts[0]
            if not hasattr(part, "function_response"):
                raise RuntimeError(f"call_function didn’t return a function_response for {fc.name}")
            
            if flag_verbose:
                print(f"-> {fc_result.parts[0].function_response.response}")
        
        print(response.text)
    else:
        print(response.text)
        print("No function calls were returned.")
    
if __name__ == "__main__":
    main()