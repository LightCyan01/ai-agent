import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
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
    
    messages = [types.Content(role="User", parts=[types.Part(text=user_prompt)])]
    response = client.models.generate_content(model='gemini-2.0-flash-001', contents=messages)
    usage = response.usage_metadata
    
    if flag_verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {usage.prompt_token_count}")
        print(f"Response tokens: {usage.candidates_token_count}")
    
if __name__ == "__main__":
    main()