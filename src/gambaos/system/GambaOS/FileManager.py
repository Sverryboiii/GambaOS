import os

def resource_path(relative_path):
    return os.path.join(os.path.join(
    str(os.getenv("APPDATA")) if os.name == "nt"\
        else os.path.join(os.path.expanduser("~"), ".config"), f"GambaOS-Sverryboiii/src/gambaos/{relative_path}"
    ))