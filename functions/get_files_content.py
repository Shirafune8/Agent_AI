import os
from google.genai import types
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    # Get absolute paths relative to the injected working_directory
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Guardrail: don't read files outside of the working directory.
    if not os.path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    # Check if file exists and is a regular file
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{abs_file_path}"'
    
    # Build the string representing the contents of the file, do not exceed MAX_CHARS characters.
    try:
        with open(abs_file_path, 'r') as file:
            content = file.read(MAX_CHARS)
            if file.read(1):
                content += f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return content

    except Exception as e:
        return f"Error: Unable to read contents of the file. {str(e)}"
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the contents of the specified file, relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)