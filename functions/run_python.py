import os
import subprocess

def run_python_file(working_directory, file_path):
    # Get absolute paths
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Error if the file_path is outside the working_directory
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    # Check if file_path exists
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'

    # Check if file exists and is python file.
    if not os.path.isfile(abs_file_path) and file_path.lower().endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    # Execute the python file.
    try:
        result = subprocess.run(
            ["python", os.path.basename(abs_file_path)],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=abs_working_dir
        )

        if result.returncode != 0:
            return f"Process exited with code {result.returncode}"

        output_lines = []

        if result.stdout.strip():
            output_lines.append(f"STDOUT:\n{result.stdout.strip()}")
        if result.stderr.strip():
            output_lines.append(f"STDERR:\n{result.stderr.strip()}")
        if result.returncode != 0:
            output_lines.append(f"Process exited with code {result.returncode}")

        if output_lines:
            return "\n".join(output_lines)
        else:
            return "No output produced."
    except Exception as e:
        return f"Error: executing Python file: {e}"