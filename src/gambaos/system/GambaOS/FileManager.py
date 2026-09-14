import os

appdata_path = str(os.getenv("APPDATA")) if os.name == "nt"\
        else os.path.join(os.path.expanduser("~"), ".config")

def resource_path(relative_path):
    return os.path.join(
        appdata_path, f"GambaOS-Sverryboiii/src/gambaos/{relative_path}"
    )

def project_level_path(relative_path):
    return os.path.join(
        appdata_path, f"GambaOS-Sverryboiii/src/{relative_path}"
    )