import os
from google.genai import types

def write_file(working_directory, file_path, content):
    # Get absolute paths
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Guardrail: don't write files outside of the working directory.
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{abs_file_path}" as it is outside the permitted working directory'
    
    # Ensure the directory for the file exists
    try:
        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
    except Exception as e:
        return f"Error: Unable to create directories for the file. {str(e)}"
    
    # Write content to file
    try:
        with open(abs_file_path, "w") as file:
            file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: Unable to write to the file. {str(e)}"
    

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to the specified file path (relative to the working directory). Overwrites existing files.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write into the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)
