import os
from .config import MAX_FILE_CHARS

def get_file_content(working_directory, file_path):
    file_full_path = os.path.join(working_directory, file_path)
    abs_file_full_path = os.path.abspath(file_full_path)
    abs_working_directory = os.path.abspath(working_directory)
    if not abs_file_full_path.startswith(abs_working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(abs_file_full_path, "r") as f:
            file_content_string = f.read(MAX_FILE_CHARS)
            extra_char = f.read(1)
            if extra_char:
                file_content_string += f'[...File "{file_path}" truncated at 10000 characters]'
            return file_content_string
    except Exception as e:
        return f"Error: {str(e)}"