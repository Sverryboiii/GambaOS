from src.gambaos.system.GambaOS.FileManager import project_level_path
from src.gambaos.system.gambapyroprism.runtime import execute as run_gpp
import sverpykit as spk, os

window: spk.Window

text_box: spk.TextBlock

def load_index(server: str):
    if not os.path.exists(server):
        text_box.change_text(f"Error: Page '{server.split('/')[-1]}' not found!")
        return
    with open(f"{server}/index.gpp", "r") as f:
        run_gpp(f.read(), text_box)

def load_page(web_page: str):
    text_box.change_text("")

    server = project_level_path(f"external_servers/{web_page}")

    load_index(server)