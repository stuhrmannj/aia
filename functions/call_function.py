from functions.get_files_info import *
from functions.get_file_content import *
from functions.run_python import *
from functions.write_file import *

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    func_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }
    func = func_map.get(function_call_part.name)
    if func is None:
        return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"Error": f"Unknown function: {function_call_part.name}"},
            )
        ],
    )

    # make a copy of the args
    args = function_call_part.args.copy()
    # add working_directory to the copied args
    args["working_directory"] = "./calculator"

    function_result = func(**args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": function_result},
            )
        ],
    )