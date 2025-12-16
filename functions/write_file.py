import os
from google.genai import types
def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_path = os.path.abspath(os.path.join(working_dir_abs, file_path))
        if not target_file_path.startswith(working_dir_abs):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(target_file_path):
            try:
                os.makedirs(os.path.dirname(target_file_path), exist_ok=True)
            except Exception as e:
                return f"Error: creating directory: {e}"
        if os.path.exists(target_file_path) and os.path.isdir(target_file_path):
            return f'Error: "{file_path} is a directory, not a file'
        with open(target_file_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to a file relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write into the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)