import os, subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run python file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file": types.Schema(
                type=types.Type.STRING,
                description="Run python file.",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    wd_abs = os.path.abspath(working_directory)
    target_abs = os.path.abspath(os.path.join(working_directory,file_path))

    if not target_abs.startswith(wd_abs):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_abs):
        return f'Error: File "{file_path}" not found.'
    
    if not target_abs.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        completed_process = subprocess.run(["python", target_abs, *args], timeout=30, capture_output=True, text=True)
        return_string = ""
        if completed_process.stdout:
            return_string += f"STDOUT: {completed_process.stdout}"
        
        if completed_process.stderr:
            if return_string:
                return_string += " "
            return_string += f"STDERR: {completed_process.stderr}"

        if completed_process.returncode != 0:
            if return_string:
                return_string += " "
            return_string = f"Process exited with code {completed_process.returncode}"
        
        if not return_string:
            return f'No output produced'
        return return_string

    except Exception as e:
        return f"Error: executing Python file: {e}"

