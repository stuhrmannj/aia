import os

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    abs_full_path = os.path.abspath(full_path)
    abs_working_directory = os.path.abspath(working_directory)
    if not abs_full_path.startswith(abs_working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(abs_full_path):
        return f'Error: "{directory}" is not a directory'
    try:
        dir_contents = os.listdir(abs_full_path)
    except Exception as e:
        return f'Error: Unable to list directory items: {e}'
    content_list = []
    for item in dir_contents:
        item_path = os.path.join(abs_full_path, item)
        try:
            item_size = os.path.getsize(item_path)
        except Exception as e:
            return f'Error: Unable to determine item size: {e}'
        try:
            item_is_dir = os.path.isdir(item_path)
        except Exception as e:
            return f'Error: Unable to determine item type: {e}'
        item_string = f'- {item}: file_size={item_size}, is_dir={item_is_dir}'
        content_list.append(item_string)
    return "\n".join(content_list)