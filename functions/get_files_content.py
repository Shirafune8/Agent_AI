import os

def get_file_content(working_directory, file_path):
    # Get absolute paths
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(file_path)

    # Guardrail: don't read files outside of the working directory.
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{abs_file_path}" as it is outside the permitted working directory'
    
    # Check if file exists and is a regular file
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{abs_file_path}"'
    
    # Build the string representing the contents of the file
    try:
        with open(abs_file_path, 'r') as file: 
            content = file.read()
        
        # Truncate if content exceeds 10,000 characters
        if len(content) > 10000:
            content = content[:10000] + f'\n[...File "{abs_file_path}" truncated at 10000 characters]'
        return content

    except Exception as e:
        return f"Error: Unable to read contents of the file. {str(e)}"