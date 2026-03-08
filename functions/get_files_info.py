import os
from google.genai import types
import subprocess
import json

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

# New: get_file_content declaration
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

# New: run_python_file declaration
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

# New: write_file declaration
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

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
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

def _abs_within_working(working_directory, target_path):
    abs_working = os.path.abspath(working_directory)
    abs_target = os.path.abspath(os.path.join(working_directory, target_path))
    return abs_working, abs_target, abs_target.startswith(abs_working)

def get_file_content(working_directory, file_path):
    abs_working, abs_target, within = _abs_within_working(working_directory, file_path)
    if not within:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_target):
        return f'Error: "{file_path}" does not exist'
    if not os.path.isfile(abs_target):
        return f'Error: "{file_path}" is not a file'
    try:
        with open(abs_target, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except Exception as e:
        return f"Error: Unable to read file '{file_path}'. {str(e)}"

def run_python_file(working_directory, file_path, args=None):
    abs_working, abs_target, within = _abs_within_working(working_directory, file_path)
    if not within:
        return f'Error: Cannot run "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_target):
        return f'Error: "{file_path}" does not exist'
    if not os.path.isfile(abs_target):
        return f'Error: "{file_path}" is not a file'
    cmd = [sys.executable, abs_target] + (args or [])
    try:
        completed = subprocess.run(
            cmd,
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=30
        )
        result = {
            "exit_code": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        }
        return json.dumps(result)
    except subprocess.TimeoutExpired as e:
        return json.dumps({"exit_code": -1, "stdout": e.stdout or "", "stderr": f"Timeout: {str(e)}"})
    except Exception as e:
        return f"Error: Failed to run '{file_path}'. {str(e)}"

def write_file(working_directory, file_path, content):
    abs_working, abs_target, within = _abs_within_working(working_directory, file_path)
    if not within:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    try:
        parent = os.path.dirname(abs_target)
        if parent and not os.path.exists(parent):
            os.makedirs(parent, exist_ok=True)
        with open(abs_target, "w", encoding="utf-8") as f:
            f.write(content)
        return f'Success: Wrote {len(content)} bytes to "{file_path}"'
    except Exception as e:
        return f'Error: Failed to write to "{file_path}". {str(e)}'