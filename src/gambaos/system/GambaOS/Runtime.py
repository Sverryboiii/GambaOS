from src.gambaos.system.GambaOS import FileManager, Config
import pygame, sverpykit as spk, os, importlib
from typing import Callable
from datetime import datetime

logging_file = FileManager.project_level_path("../logs/RuntimeLogs.log")

def quit_gambaos():
    log_message("INFO", "Quitting GambaOS!")
    spk.quit_game()

def launch_application(application_path: str, run_function: str | None = None, *function_args):
    module = importlib.import_module(f"src/gambaos/system/applications/{application_path}/main".replace("/", "."))
    module.main()
    if not run_function:
        return
    functions = importlib.import_module(f"src/gambaos/system/applications/{application_path}/Functions".replace("/", "."))
    getattr(functions, run_function)(*function_args)

def get_application_buttons() -> list[spk.Button]:
    application_paths = os.listdir(FileManager.resource_path("system/applications"))
    applications: list[spk.Button] = []
    count = 0
    for path in application_paths:
        applications.append(
            spk.Button(
                rect=pygame.Rect(
                    10,
                    10 + 40*count,
                    Config.screen.get_width() / 5 - 20,
                    30
                ),
                button_color=(100, 100, 100),
                surface=spk.render_text(f"{path.replace("_", " ").title()}"),
                display=Config.screen,
                function=launch_application,
                application_path = path
            )
        )
        count += 1
    return applications

def log_message(message_type: str = "INFO", message: str = "") -> None:
    path = "/".join(logging_file.split("/")[:-1])
    print(path)
    if not os.path.exists(path):
        print("File not found")
        os.makedirs(path)

    timestamp = datetime.now().strftime("%Y-%m-%d (%H:%M.%S)")
    log_msg = f"({timestamp}) [{message_type}]: >> {message}\n"

    with open(logging_file, "a") as f:
        f.write(log_msg)
    return
log_message("INFO", "Starting up GambaOS.")