import os
from config import MAX_CHARS
from google.genai import types
def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_path = os.path.abspath(os.path.join(working_dir_abs, file_path))
        if not target_file_path.startswith(working_dir_abs):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file_path):
            return f'Error: file not found or is not a regular file: "{file_path}'
        with open(target_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if os.path.getsize(target_file_path) > MAX_CHARS:
                file_content_string = file_content_string + f'[...File "{file_path}" truncated at 10000 characters'
        return file_content_string
    except Exception as e:
        return f"Error: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Lists the content of a file in one concatenated string. If over max chars given, adds ...File \"file_path\" truncated at 10000 characters",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to read the contents of the file from, relative to the current working directory. Must provide valid file path relative to current working directory",
            ),
        },
    ),
)