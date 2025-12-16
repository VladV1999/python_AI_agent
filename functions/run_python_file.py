import os
import subprocess
from google.genai import types
def run_python_file(working_directory, file_path, args=[]):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.abspath(os.path.join(working_dir_abs, file_path))
        if not file_path_abs.startswith(working_dir_abs):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(file_path_abs):
            return f'Error: File "{file_path}" not found.'
        parts = file_path.split(".")
        extension = parts[-1]
        if not extension == "py":
            return f'Error: "{file_path}" is not a Python file.'
        commands = ["python", file_path_abs]
        if len(args) > 0:
            commands.extend(args)
        result = subprocess.run(commands, timeout=30, capture_output=True, cwd=working_dir_abs, text=True)
        output_parts = []
        if result.stdout:
            output_parts.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output_parts.append(f"STDERR:\n{result.stderr}")
        exit_code_status = result.returncode
        if not exit_code_status == 0:
            output_parts.append(f"Process exited with code {str(exit_code_status)}")
        result = "\n".join(output_parts)
        if not output_parts:
            return "No output produced"
        return result
    except Exception as e:
        return f"Error: executing python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file, strictly constricted to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The python file to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional CLI args to pass to the python file.",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
        required=["file_path"],
    ),
)