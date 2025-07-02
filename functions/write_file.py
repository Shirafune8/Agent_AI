import os

def write_file(working_directory, file_path, content):
    # Get absolute paths
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(file_path)

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
        return f'Successfully wrote to "{abs_file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: Unable to write to the file. {str(e)}"
    