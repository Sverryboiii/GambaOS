from src.gambaos.system.applications.web_explorer import Functions, Config as WebConfig
import sverpykit as spk, pygame

def add_layers():

    Functions.window = spk.add_layer(
        "window",
        rectangle=pygame.Rect(*Functions.rect),
        components=Functions.base_components,
        color=WebConfig.window_color
    )

    Functions.load_page("")