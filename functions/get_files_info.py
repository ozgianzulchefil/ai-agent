import os

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    wd_abs = os.path.abspath(working_directory)
    target_abs = os.path.abspath(full_path)

    if not target_abs.startswith(wd_abs):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    elif not os.path.isdir(target_abs):
        return f'Error: "{directory}" is not a directory'
    try:    
        file_list = os.listdir(target_abs)
        lines = []
        for file in file_list:
            entry_path = os.path.join(target_abs, file)
            is_dir=os.path.isdir(entry_path)
            size = os.path.getsize(entry_path)
            lines.append(f"- {file}: file_size={size} bytes, is_dir={is_dir}")
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"