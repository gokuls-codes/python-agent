import os
import subprocess
from google.genai import types

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

def run_python_file_in_docker(working_directory, file_path, args=[]):

    abs_working_directory = os.path.abspath(working_directory)

    target_file = os.path.normpath(os.path.join(abs_working_directory, file_path))

    valid_target_file = os.path.commonpath([abs_working_directory, target_file]) == abs_working_directory

    if not valid_target_file:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_file):
        return f'Error: "{file_path}" does not exist or is not a regular file'

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'

    IMAGE = "python:3.14.3-slim-trixie"

    docker_command = [
        "docker", "run", "--rm",
        "--network", "none",           # No internet access
        "--memory", "256m",            # RAM limit
        "--cpus", "0.5",               # CPU limit
        "-v", f"{abs_working_directory}:/app:rw", # Mount workspace as /app
        "-w", "/app",                  # Set working directory inside container
        IMAGE,
        "python", file_path            # Run the relative path inside /app
    ]
    docker_command.extend(args)

    try:
        # Note: We use a timeout to prevent infinite loops from hanging your Python script
        output = subprocess.run(docker_command, capture_output=True, text=True, timeout=35)
        
        stdout = output.stdout
        stderr = output.stderr
        
        if not stdout and not stderr:
            return "Execution finished with no output (STDOUT/STDERR empty)."

        response = f"STDOUT:\n{stdout}\nSTDERR:\n{stderr}"
        if output.returncode != 0:
            response += f"\nProcess exited with code {output.returncode}"
        return response

    except subprocess.TimeoutExpired:
        return "Error: Execution timed out (Possible infinite loop in agent code)."
    except Exception as e:
        return f"Error executing in sandbox: {str(e)}"


schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description="Runs the given python file using the list of arguments provided",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="Path to the python file to execute, relative to the working directory",
                    ),
                "args": types.Schema(
                    type=types.Type.ARRAY,
                    description="List of arguments to be passed to the python file",
                    items=types.Schema(type=types.Type.STRING)
                    )
                },
            required=["file_path"]
            )
        )
