import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    abs_path = os.path.abspath(working_directory)
    filepath = os.path.abspath(os.path.join(abs_path, file_path))
    try:
        if not filepath.startswith(abs_path):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(filepath):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(filepath, "r") as f:
            file_content_string = f.read()
        
        if len(file_content_string) > MAX_CHARS:
            file_content_string = file_content_string[:MAX_CHARS] + f' "{file_path}" truncated at 10000 characters'
   
        return file_content_string

    except Exception as e:
        return f"Error: {e}"

