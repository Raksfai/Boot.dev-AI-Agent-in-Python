import os
from config import MAX_CHARS
from google.genai import types

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

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads and returns the first {MAX_CHARS} characters of the content from a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="The working directory path (usually '.')",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose content should be read, relative to the working directory.",
            ),
        },
        required=["working_directory", "file_path"],
    ),
)
