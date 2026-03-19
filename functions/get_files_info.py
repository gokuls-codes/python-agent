import os

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
