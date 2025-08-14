import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if os.path.isdir(full_path) == False:
        return f'Error: "{directory}" is not a directory'
    try:
        list_of_content = os.listdir(full_path)
        line = []
        for item in list_of_content:
            item_path = os.path.join(full_path, item)
            line.append(f"- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}")
    except Exception as e:
        return f"Error: {str(e)}"
    return "\n".join(line)

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

