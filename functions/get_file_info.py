import os
from google.genai import types

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
            
        abs_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_path, directory))

        valid_target_dir = os.path.commonpath([abs_path, target_dir]) == abs_path

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        elif not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'


        contents = os.listdir(target_dir)
        results = []

        for i in contents:
            item_path = os.path.join(target_dir,i)
            is_dir = os.path.isdir(item_path)
            file_size = os.path.getsize(item_path)
            results.append(f'- {i}: file_size={file_size}, is_dir={is_dir}')
    
        if directory == ".":
            header = f'Result for current directory:'
        else:
            header = f'Result for {directory} directory'

        return header + "\n" + "\n".join(results)
    except Exception as e:
        return f'Error: , {e}'


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)"
            ),
        },
    ),
)