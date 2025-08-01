import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    file_full_path = os.path.join(working_directory, file_path)
    abs_file_full_path = os.path.abspath(file_full_path)
    abs_working_directory = os.path.abspath(working_directory)
    if not abs_file_full_path.startswith(abs_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_file_full_path):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        completed_process = subprocess.run(
            ["python", file_path] + args,
            timeout=30,
            capture_output=True,
            text=True,
            cwd=working_directory
        )
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
    # Get the outputs
    stdout_output = completed_process.stdout
    stderr_output = completed_process.stderr
    return_code = completed_process.returncode

    # Start building the result string
    result_parts = []

    # Add stdout if it exists
    if stdout_output:
        result_parts.append(f"STDOUT:\n{stdout_output}")

    # Add stderr if it exists  
    if stderr_output:
        result_parts.append(f"STDERR:\n{stderr_output}")

    # Add exit code message if process failed
    if return_code != 0:
        result_parts.append(f"Process exited with code {return_code}")

    # If no output at all, return the no output message
    if not result_parts:
        return "No output produced."

    # Join all parts with newlines and return
    return "\n".join(result_parts)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a python file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path in the working directory.",
            ),
        },
    ),
)
    
