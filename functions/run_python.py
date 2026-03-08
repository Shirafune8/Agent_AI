import os
from google.genai import types
import subprocess
import sys

def run_python_file(working_directory, file_path, args=None):
    # Get absolute paths
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Error if the file_path is outside the working_directory
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    # Check if file_path exists
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'

    # Ensure it's a regular file
    if not os.path.isfile(abs_file_path):
        return f'Error: "{file_path}" is not a regular file.'

    # Execute the python file.
    try:
        cmd = [sys.executable, abs_file_path] + (args or [])
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=abs_working_dir
        )

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

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file in the working directory with optional arguments and returns stdout, stderr, and exit code.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="An argument to pass to the script.",
                ),
                description="Optional list of string arguments to pass to the script.",
            ),
        },
        required=["file_path"],
    ),
)