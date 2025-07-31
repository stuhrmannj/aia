import os

def write_file(working_directory, file_path, content):
    file_full_path = os.path.join(working_directory, file_path)
    abs_file_full_path = os.path.abspath(file_full_path)
    abs_working_directory = os.path.abspath(working_directory)
    if not abs_file_full_path.startswith(abs_working_directory):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_file_full_path):
        os.makedirs(os.path.dirname(abs_file_full_path), exist_ok=True)
    try:
        with open(abs_file_full_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"