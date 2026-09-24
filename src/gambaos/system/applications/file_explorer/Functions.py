from src.gambaos.system.GambaOS import FileManager, Config
import os, sverpykit as spk, pygame

window: spk.Window

current_directory = "user"

def change_directory(directory: str):
    global current_directory
    if directory == "..":
        current_directory = "/".join(current_directory.split("/")[:-1])
    else:
        current_directory = current_directory + "/" + directory

    reset_file_buttons()

def reset_file_buttons():
    files: list = get_files(current_directory)

    window.components = [
        component for component in window.components\
        if not isinstance(component, spk.Button)
    ]

    window.components.append(
        spk.Button(
            rect=pygame.Rect(10, 10, 40, 40),
            button_color=(50, 50, 50),
            surface=spk.render_text(
                text="..",
                name="tiny"
            ),
                display=Config.screen,
                function=change_directory,
                rounding=5,
                directory=".."
        )
    )

    for c, file in enumerate(files):
        window.components.append(
            spk.Button(
                rect=pygame.Rect(
                    60 + c*50,
                    10, 40, 40
                ),
                button_color=(50, 50, 50),
                surface=spk.render_text(
                    text=file,
                    name="tiny"
                ),
                display=Config.screen,
                function=change_directory,
                rounding=5,
                directory=file
            )
        )

def get_files(directory: str) -> list[str] | list[bytes]:
    return os.listdir(FileManager.resource_path(directory))