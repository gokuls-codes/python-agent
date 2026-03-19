import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):

    abs_working_directory = os.path.abspath(working_directory)

    target_file = os.path.normpath(os.path.join(abs_working_directory, file_path))

    valid_target_file = os.path.commonpath([abs_working_directory, target_file]) == abs_working_directory

    if not valid_target_file:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_file):
        return f'Error: "{file_path}" does not exist or is not a regular file'

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'

    try:
        command = ["python", target_file]
        command.extend(args)
        output = subprocess.run(command, cwd=abs_working_directory, capture_output=True, timeout=30, text=True)

        final_response = f"""
    STDOUT: {output.stdout}
    STDERR: {output.stderr}
    """ 
        
        if output.stdout == "" and output.stderr == "":
            final_response = "No output produced"

        if output.returncode != 0:
            final_response += f"Process exited with code {output.returncode}"

        return final_response

    except Exception as e:
        return f'Error: executing python file: {e}'
