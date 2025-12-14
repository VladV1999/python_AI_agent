import os
def get_files_info(working_directory, directory="."):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    try:
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        lines = []
        for entry_name in os.listdir(target_dir):
            entry_path = os.path.join(target_dir, entry_name)
            is_dir = os.path.isdir(entry_path)
            file_size = os.path.getsize(entry_path)
            str_to_append = f"- {entry_name}: file_size={file_size} bytes, is_dir={is_dir}"
            lines.append(str_to_append)
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"