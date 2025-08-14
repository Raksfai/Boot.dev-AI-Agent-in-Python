import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    try:
        abs_path = os.path.abspath(working_directory)
        target_dir = os.path.abspath(os.path.join(abs_path, file_path))
        if not target_dir.startswith(abs_path):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(target_dir):
            return f'Error: File "{file_path}" not found.'

        if not target_dir.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        result = subprocess.run(["python", target_dir] + args, capture_output=True, timeout=30, cwd=abs_path)
        list_item = []
        output = ''
        decoded_stdout = result.stdout.decode('utf-8')
        decoded_stderr = result.stderr.decode('utf-8')
 
        if decoded_stdout == "" and decoded_stderr == "":
            return "No output produced."

        if decoded_stdout != "":
            list_item.append(f"STDOUT: {decoded_stdout}")

        if decoded_stderr != "":
            list_item.append(f"STDERR: {decoded_stderr}")
        
        if result.returncode != 0:
            list_item.append(f" Process exited with code {result.returncode}")
        concat = "\n".join(list_item)

        return concat

    except Exception as e:
        return f"Error: executing Python file: {e}" 

