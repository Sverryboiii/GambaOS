from src.gambaos.system.applications.web_explorer import Functions
from src.gambaos.system.GambaOS import Config
import sverpykit as spk, pygame

def add_layers():

    rect = (
        Config.screen.get_width()/2 - Config.screen.get_width()/4,
        Config.screen.get_height()/2 - Config.screen.get_height()/4,
        Config.screen.get_width()/2,
        Config.screen.get_height()/2
    )

    searchbar_height = 30

    Functions.text_box = spk.TextBlock(
        pygame.Rect(0, searchbar_height, rect[2], rect[3]-searchbar_height),
        ""
    )

    widgets = Functions.get_widgets()

    Functions.window = spk.add_layer(
        "window",
        rectangle=pygame.Rect(*rect),
        components=[
            spk.SearchBar(
                rect=pygame.Rect(
                    0, 0, rect[2], searchbar_height
                ),
                display=Config.screen,
                function=Functions.load_page
            ),
            Functions.text_box,
            *widgets
        ]
    )