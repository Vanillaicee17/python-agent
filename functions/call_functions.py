from functions.get_file_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import schema_run_python_file, run_python_file

from google.genai import types

from collections.abc import Callable
import copy

available_functions = types.Tool(
    function_declarations=[schema_get_files_info,schema_run_python_file,schema_get_file_content
                           ,schema_write_file],
)

function_map: dict[str, Callable[..., str]] = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "write_file": write_file,
    "run_python_file": run_python_file
}

def call_function(function_call: types.FunctionCall, verbose: bool = False) -> types.Content:
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")
    
    function_name = function_call.name or ""

    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"unknown function: {function_name}"}
                )
            ]
        )
    
    args = copy.copy(function_call.args) if function_call.args else {}

    args["working_directory"] = "./calculator"

    func = function_map[function_name]

    function_result = func(**args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
