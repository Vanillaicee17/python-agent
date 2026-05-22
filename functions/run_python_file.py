import os
import subprocess
from google.genai import types

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        abs_path = os.path.abspath(working_directory)
        joined_path = os.path.join(abs_path, file_path)

        target_dir = os.path.normpath(joined_path)

        validate_path = os.path.commonpath([abs_path, target_dir]) == abs_path

        if not validate_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_dir.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ['python', target_dir]

        if args:
            command.extend(args)

        response = subprocess.run(command, cwd=abs_path, capture_output=True, text=True, timeout=30)


        output = []

        if response.returncode != 0:
            output.append(f"Process exited with code {response.returncode}")
        
        if response.stdout:
            output.append(f"STDOUT:\n{response.stdout}")            

        if response.stderr:
            output.append(f"STDERR:\n{response.stderr}")   

        if not response.stdout and not response.stderr:
            output.append("No output produced")  

        return "\n".join(output)         
    except Exception as e:
        return f'Error: {e}'
    

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file relative to the working directory with optional command line arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute"
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING
                ),
                description="Optional command line arguments to pass to the Python file"
            ),
        },
        required=["file_path"],
    ),
)
