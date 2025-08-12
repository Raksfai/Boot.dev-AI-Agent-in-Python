import os

def write_file(working_directory, file_path, content):
    abspath = os.path.abspath(working_directory)
    filepath = os.path.abspath(os.path.join(abspath, file_path))
    try:
        if not filepath.startswith(abspath):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(filepath):
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error {e}"
