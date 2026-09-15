import os, json

appdata_path = str(os.getenv("APPDATA")) if os.name == "nt"\
        else os.path.join(os.path.expanduser("~"), ".config")

def resource_path(relative_path: str) -> str:
    return os.path.join(
        appdata_path, f"GambaOS-Sverryboiii/src/gambaos/{relative_path}"
    )

def project_level_path(relative_path: str) -> str:
    return os.path.join(
        appdata_path, f"GambaOS-Sverryboiii/src/{relative_path}"
    )

def json_read(path: str) -> list | dict:
    with open(path, "r") as f:
        return json.load(f)

def json_write(path: str, obj: list | dict) -> None:
    with open(path, "w") as f:
        json.dump(obj, f, indent=4)

def json_update(path: str, obj: list | dict) -> None:
    with open(path, "r") as f:
        data = json.load(f)

    if not isinstance(obj, type(data)):
        raise TypeError(f"Failed to update json file! Json file is type '{type(data)}', but inserted object is type '{type(obj)}'!")

    if isinstance(obj, dict):
        for var, val in obj.items():
            data[var] = [val]
    else:
        for val in obj:
            data.append(val)

    with open(path, "w") as f:
        json.dump(data, f, indent=4)