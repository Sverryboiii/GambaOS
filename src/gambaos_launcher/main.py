import pygame, sverpykit as spk, os, shutil, sys, importlib
from pathlib import Path

screen = spk.set_display(500, 500)
pygame.display.set_caption("GambaOS Launcher")
font = spk.set_font()

base = Path(__file__).resolve().parent
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, f"../{relative_path}")
    return os.path.join(base, f"../{relative_path}")

reset = False
def toggle_reset():
    global reset
    reset = not reset

config = os.path.join(
    str(os.getenv("APPDATA")) if os.name == "nt"\
        else os.path.join(os.path.expanduser("~"), ".config"), "GambaOS"
)

if not os.path.exists(config):
    shutil.copytree(resource_path("gambaos"), config, ignore=shutil.ignore_patterns("*.pyc", "__pycache__"))

def start_gamba_os():
    global reset
    if reset:
        shutil.rmtree(config)
        shutil.copytree(resource_path("gambaos"), config, ignore=shutil.ignore_patterns("*.pyc", "__pycache__"))
    sys.path.append(config)
    importlib.import_module("system.GambaOS.main")

ui = [
    spk.Button(
        rect=pygame.Rect(
            screen.get_width()/2 - 100,
            screen.get_height() - 100,
            200, 50
        ),
        button_color=(50, 50, 50),
        surface=spk.render_text("RUN"),
        display=screen,
        function=start_gamba_os,
        rounding=3
    ),
    spk.Button(
        rect=pygame.Rect(
            screen.get_width()/2 - 100,
            10, 200, 50
        ),
        button_color=(50, 50, 50),
        surface=spk.render_text("RESET", color=(255, 0, 0)),
        display=screen,
        function=toggle_reset,
        rounding=3
    )
]

def frame():
    global reset
    screen.blit(
        spk.render_text("Warning! Reset when RUN is pressed!" if reset else "", color=(255, 200, 0)),
        (
            0, screen.get_height()-25
        )
    )
    [part.update() for part in ui]

spk.set_frame_method(frame)
spk.start()