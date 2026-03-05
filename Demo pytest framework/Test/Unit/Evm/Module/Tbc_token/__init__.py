from pathlib import Path
from Setting import path_dir_log

if not Path(path_dir_log).is_dir():
    raise exit(f"Directory not found: {path_dir_log}")

