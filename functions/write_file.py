import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write text content to a file at the given relative path.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file": types.Schema(
                type=types.Type.STRING,
                description="Relative path of the file to write.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text to write into the file.",
            )
        },
        required=["file","content"]
    ),
)


def write_file(working_directory, file_path, content):
    wd_abs = os.path.abspath(working_directory)
    target_abs = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_abs.startswith(wd_abs):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        parent_dir = os.path.dirname(target_abs)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)
            # os.makedirs(target_abs)
        with open(target_abs, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"