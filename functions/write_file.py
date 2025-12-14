import os
def write_file(working_directory, file_path, content):
    working_dir_abs = os.path.abspath(working_directory)
    target_file_path = os.path.abspath(os.path.join(working_dir_abs, file_path))

    if not target_file_path.startswith(working_dir_abs):
        return f'Error: Cannote write to "{file_path}" as it is outside the permitted working directory'
    