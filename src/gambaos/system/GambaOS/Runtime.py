from src.gambaos.system.GambaOS import FileManager, Config
import pygame, sverpykit as spk, os, importlib

def launch_application(application_path: str):
    module = importlib.import_module(f"src/gambaos/system/applications/{application_path}/main".replace("/", "."))
    module.main()

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