import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

def main():
    print("Hello from aia!")
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
    prompt = sys.argv[1]
    if len(prompt) < 2:
        print("No prompt provided.  Program Terminated.")
        sys.exit(1)
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )    
    messages = [types.Content(role="user", parts=[types.Part(text = prompt)])]
    response = client.models.generate_content(
        model = "gemini-2.0-flash-001",
        contents = messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        )
    )
    user_prompt = sys.argv[1]
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
        print(f"User prompt:  {user_prompt}")
        print(f"Prompt tokens:  {prompt_tokens}")
        print(f"Response tokens:  {response_tokens}")

    function_call = response.function_calls
    if function_call:
        for function_call_part in function_call:
            # Use the verbose flag depending on command line
            verbose = len(sys.argv) > 2 and sys.argv[2] == "--verbose"
            function_call_result = call_function(function_call_part, verbose=verbose)

            # Now extract and print the result (or error) from function_call_result
            parts = function_call_result.parts
            if parts and hasattr(parts[0], "function_response"):
                response = parts[0].function_response.response
                if "result" in response and verbose:
                    print(f"-> {response['result']}")
                elif "error" in response:
                    print(f"Error calling function: {response['error']}")
                # You do not need to print result if not verbose (the lesson examples only print result when verbose)
            else:
                raise Exception("Missing function response in tool output.")

if __name__ == "__main__":
    main()
