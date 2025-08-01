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

When a user asks a question or makes a request, you MUST use the available function/tool calls to interact with the project and investigate on your own. Do not ask the user questions to clarify which files or code to look at. Instead, always start by listing files in the directory and then reading or executing files as needed to fulfill the user request.

You may only use the allowed function/tool calls for any file system or code actions. Do not describe your plan, perform the actions!
- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. Never ask the user to provide more detail—use the tools and your reasoning to figure it out yourself.
I reiterate...do not describe your plan.  Execute the plan until complete!
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

    MAX_ITERATIONS = 20
    done = False

    for _ in range(MAX_ITERATIONS):
        response = client.models.generate_content(
            model = "gemini-2.0-flash-001",
            contents = messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            )
        )

        for candidate in response.candidates:
            messages.append(candidate.content)
            for part in candidate.content.parts:
                # If the model is requesting a tool/function call
                if getattr(part, "function_call", None) is not None:
                    function_call_part = part.function_call
                    print(f"- Calling function: {function_call_part.name}")
                    verbose = len(sys.argv) > 2 and sys.argv[2] == "--verbose"
                    function_call_result = call_function(function_call_part, verbose=verbose)
                    tool_msg = types.Content(
                        role="tool",
                        parts=function_call_result.parts
                    )
                    messages.append(tool_msg)
                    # Optionally, print function results if verbose
                    parts_func = function_call_result.parts
                    if parts_func and hasattr(parts_func[0], "function_response"):
                        function_response_data = parts_func[0].function_response.response
                        if "result" in function_response_data and verbose:
                            print(f"-> {function_response_data['result']}")
                        elif "error" in function_response_data:
                            print(f"Error calling function: {function_response_data['error']}")
                # If the model is providing a final text answer
                elif hasattr(part, "text") and part.text:
                    print(part.text)
                    done = True
                    break
            if done:
                break
        if done:
            break

    if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
        user_prompt = sys.argv[1]
        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count
        print(f"User prompt:  {user_prompt}")
        print(f"Prompt tokens:  {prompt_tokens}")
        print(f"Response tokens:  {response_tokens}")

if __name__ == "__main__":
    main()
