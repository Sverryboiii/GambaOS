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

    server = FileManager.project_level_path(f"external_servers/{web_address}")

    load_index(server)