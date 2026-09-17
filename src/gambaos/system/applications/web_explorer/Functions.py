from src.gambaos.system.GambaOS import FileManager, Config
from src.gambaos.system.GambaOS.integrated.gml.runtime import execute as run_gpp
from src.gambaos.system.applications.web_explorer import Config as WebConfig
import sverpykit as spk, os, pygame

window: spk.Window

text_box: spk.TextBlock

def get_widgets():

    cookies_file = FileManager.resource_path("system/applications/web_explorer/cookies.json")

    if not os.path.exists(cookies_file):
        return []

    cookies: list | dict = FileManager.json_read(cookies_file)
    if isinstance(cookies, list):
        return []
    widget_cookies: dict = cookies.get("widgets", {})
    if not widget_cookies or widget_cookies == {}:
        return []

    widgets = []

    x = 0
    for name, address in widget_cookies.items():
        widgets.append(
            spk.Button(
                rect=pygame.Rect(10 + x, 100, 70, 70),
                button_color=(50, 50, 50),
                surface=spk.render_text(f"{name[0].upper()}", name="default"),
                display=Config.screen,
                function=load_page,
                rounding=10,
                web_address=address
            )
        )
        x += 75

    return widgets

def load_index(server: str):
    if not os.path.exists(server):
        text_box.change_text(f"Error: Page '{server.split('/')[-1]}' not found!")
        return
    with open(f"{server}/index.gpp", "r") as f:
        run_gpp(f.read(), text_box, window, load_page, server)

def load_page(web_address: str):
    window.components = [component for component in window.components if not isinstance(component, spk.Button)]
    window.color = WebConfig.window_color
    text_box.text_surfs = []
    text_box.text = ""
    if web_address == "":
        window.components = base_components
        text_box.add_text(
            "Welcome to the GambaOS web explorer",
            "default",
            (0, 0, 0)
        )
        return

    server = FileManager.project_level_path(f"external_servers/{web_address}")

    load_index(server)

rect = (
    Config.screen.get_width() / 2 - Config.screen.get_width() / 4,
    Config.screen.get_height() / 2 - Config.screen.get_height() / 4,
    Config.screen.get_width() / 2,
    Config.screen.get_height() / 2
)

searchbar_height = 30

text_box = spk.TextBlock(
    pygame.Rect(0, searchbar_height, rect[2], rect[3] - searchbar_height),
    ""
)

widgets = get_widgets()

base_components = [
    spk.SearchBar(
        rect=pygame.Rect(
            0, 0, rect[2], searchbar_height
        ),
        display=Config.screen,
        function=load_page,
        color=(100, 100, 100)
    ),
    text_box,
    *widgets
]