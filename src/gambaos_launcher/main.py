print("Inintializing modules...")
import io, os, shutil, zipfile, urllib.request, urllib.error, sys, importlib.util, json, pygame
from pathlib import Path
pygame.init()
print("Modules initialized")

debug = True

main_repo_url = "https://www.github.com/Sverryboiii/GambaOS/archive/refs/heads/main.zip"

appdata = os.path.join(
    str(os.getenv("LOCALAPPDATA")) if os.name == "nt"\
        else os.path.join(os.path.expanduser("~"), ".config"), "GambaOS-Sverryboiii"
)
instances_path = os.path.join(appdata, "instances")
temp_folder = os.path.join(appdata, "temp")
if not os.path.exists(temp_folder):
    os.makedirs(temp_folder)

base = Path(__file__).resolve().parent

reset: bool = False

def open_instance(instance):
    print("Starting GambaOS...")
    import sverpykit, screeninfo

    global reset
    if reset:
        return

    with open(os.path.join(temp_folder, "tmp.json"), "w") as f:
        json.dump({
            "instance": instance.split("/")[-1]
        }, f, indent=4)

    if instance in sys.path:
        sys.path.remove(instance)
    sys.path.insert(0, instance)
    spec = importlib.util.spec_from_file_location(
        "appdata_GambaOS",
        os.path.join(instance, "src/gambaos/system/GambaOS/main.py").replace("\\", "/")
    )
    gamba_os = importlib.util.module_from_spec(spec)
    sys.modules["gamba_main"] = gamba_os
    print("Starting logs from here:")
    spec.loader.exec_module(gamba_os)
    sys.path.remove(instance)

def download_gambaos_version(version: str = "vTEST-0.1.1", dest_directory: str = ""):
    # https://github.com/sverryboiii/gambaos/archive/refs/tags/vTEST-0.1.1.zip
    # Example link
    print("Downloading packets... (Do not close this window!)")

    target_dir = os.path.join(instances_path, f"{dest_directory}")

    if os.path.exists(target_dir):
        return {
            "error": "There is already an instance here!"
        }
    os.makedirs(target_dir)

    url = f"https://github.com/sverryboiii/gambaos/archive/refs/tags/{version}.zip"
    if debug:
        url = main_repo_url

    try:

        with urllib.request.urlopen(url) as response:
            repo_data = response.read()

        with zipfile.ZipFile(io.BytesIO(repo_data)) as zip_ref:

            root = zip_ref.namelist()[0].split("/")[0]
            src = os.path.join(root, "src").replace("\\", "/")

            last_part = ""

            for file in zip_ref.infolist():
                if not file.filename.startswith(src):
                    continue

                relative_path = file.filename.replace(f"{root}/", "", 1)
                target_path = os.path.join(target_dir, relative_path).replace("\\", "/")
                new_path = relative_path.split("/")[1]
                if new_path != last_part:
                    print(f"Downloading path: {new_path}")
                    last_part = new_path

                if file.is_dir():
                    os.makedirs(target_path, exist_ok=True)
                else:
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)

                    with zip_ref.open(file) as source, open(target_path, "wb") as dest:
                        shutil.copyfileobj(source, dest)

    except urllib.error.HTTPError:
        return {
            "error": "Invalid url, did you get the version correct? (If so, please report this to Sverryboiii)!"
        }
    open_instance(target_dir)
    return {}

def main():
    legal_chars = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ _-"
    while True:
        print("Press CTRL + C to exit at any time!")
        instance = input("GambaOS Instance: ")
        if any(char not in legal_chars for char in instance):
            print(f"\033[31m'{instance}' contains illegal characters! Be sure to only use 0-9, a-z, A-Z, ' ', '_' and '-'\033[0m")
            continue
        full_path = os.path.join(instances_path, instance)
        if os.path.exists(full_path):
            open_instance(full_path)
        else:
            version = input("Version: ") if not debug else ""
            payload = download_gambaos_version(version, instance)
            if payload.get("error", None):
                print(payload["error"])

if __name__ == "__main__":
    print("\n ==== Welcome To GambaOS Launcher! ==== \n")
    while True:
        pygame.init()
        if debug:
            main()
            continue
        try:
            main()
        except Exception:
            pygame.quit()
            print("\033[31m\n[Error] >> Oops something went wrong, please contact us on discord!\033[0m")
        print("Logs ended!")
