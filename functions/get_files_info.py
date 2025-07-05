import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)

def get_files_info(working_directory, directory='.'):
    # Default to working directory
    target_directory = directory if directory is not None else working_directory
    
    abs_working = os.path.abspath(working_directory)
    abs_target = os.path.abspath(os.path.join(working_directory, directory))  # Ensure relative paths are resolved
    
    # Guardrails: don't allow directories outside the working directory.
    if not abs_target.startswith(abs_working):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    # Check if directory is a valid directory
    if not os.path.isdir(abs_target):
        return f'Error: "{directory}" is not a directory'

    # Build the string representing the contents of the directory
    try:
        contents = os.listdir(abs_target)
        result = []
        for item in contents:
            item_path = os.path.join(abs_target, item)
            is_dir = os.path.isdir(item_path)
            file_size = os.path.getsize(item_path) if not is_dir else 0
            result.append(f"{item}: file_size={file_size} bytes, is_dir={is_dir}")
        return "\n".join(result)
    except Exception as e:
        return f"Error: Unable to list contents of the directory. {str(e)}"