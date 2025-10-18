import os
from config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="List file content.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file": types.Schema(
                type=types.Type.STRING,
                description="List file content.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    wd_abs = os.path.abspath(working_directory)
    target_abs = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not target_abs.startswith(wd_abs):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_abs):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(target_abs, "r") as f:
            content = f.read(MAX_CHARS + 1)
            if len(content) > MAX_CHARS:
                content = content[:MAX_CHARS] + f'[...File "{file_path}" truncated at 10000 characters]'
        return content
            
    except Exception as e:
        return f"Error: {e}"