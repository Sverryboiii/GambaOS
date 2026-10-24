from src.gambaos.system.applications.text_editor import Functions
from src.gambaos.system.GambaOS import Config
import sverpykit as spk, pygame

def add_layers():

    rect = (
            Config.screen.get_width()/2 - Config.screen.get_width()/4,
            Config.screen.get_height()/2 - Config.screen.get_height()/4,
            Config.screen.get_width()/2,
            Config.screen.get_height()/2
    )

    Functions.text_box = spk.TextBlock(
        pygame.Rect(0, 0, rect[2], rect[3]),
        ""
    )

    Functions.window = spk.add_layer(
        "window",
        pygame.Rect(*rect),
        components=[Functions.text_box]
    )