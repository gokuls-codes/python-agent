import os
from google.genai import types

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

schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="Writes the given content to the specified file, creating the file if it does not exist",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="Path to the file to write to, relative to the working directory"
                    ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="Content to write to the file"
                    )
                },
            required=["file_path", "content"]
            )
        )
