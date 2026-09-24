from src.gambaos.system.applications.file_explorer import Functions
from src.gambaos.system.GambaOS import Config
import sverpykit as spk, pygame

def add_layers():

    rect = (
        Config.screen.get_width()/2 - Config.screen.get_width()/4,
        Config.screen.get_height()/2 - Config.screen.get_height()/4,
        Config.screen.get_width()/2,
        Config.screen.get_height()/2
    )

    Functions.window = spk.add_layer(
        layer_type="window",
        rectangle=pygame.Rect(*rect),
        components=[]
    )

    Functions.reset_file_buttons()