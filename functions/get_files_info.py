import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    abs_working_directory = os.path.abspath(working_directory)
    target_directory = os.path.normpath(os.path.join(abs_working_directory, directory))

    valid_target_directory = os.path.commonpath([abs_working_directory, target_directory]) == abs_working_directory

    if not valid_target_directory:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(target_directory):
        return f'Error: "{directory}" is not a directory'

    final_response = ""
    for content in os.listdir(target_directory):
        content_path = os.path.join(target_directory, content)
        is_dir = os.path.isdir(content_path)
        size = os.path.getsize(content_path)
        final_response += f"- {content}: file_size={size}, is_dir={is_dir}\n"

    return final_response

schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
                    )
                }
            )
        )
