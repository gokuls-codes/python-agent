
import os

def write_file(working_directory, file_path, content):
    abs_working_directory = os.path.abspath(working_directory)

    target_file = os.path.normpath(os.path.join(abs_working_directory, file_path))

    valid_target_file = os.path.commonpath([abs_working_directory, target_file]) == abs_working_directory

    if not valid_target_file:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if os.path.isdir(target_file):
        return  f'Error: Cannot write to "{file_path}" as it is a directory'

    if not os.path.isfile(target_file):
        parent_dir = os.path.dirname(target_file)
        os.makedirs(parent_dir, exist_ok=True)

    with open(target_file, "w") as f:
        f.write(content)

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
