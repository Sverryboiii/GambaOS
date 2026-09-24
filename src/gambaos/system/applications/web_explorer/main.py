from src.gambaos.system.applications.web_explorer import Ui
from src.gambaos.system.GambaOS import FileManager
import os

def main():
    cookies_path = FileManager.resource_path("system/applications/web_explorer/cookies.json")
    if not os.path.exists(cookies_path):
        FileManager.json_write(cookies_path, {"widgets": {"GambaOS Info": "gww.gamba_info.gam"}})

    Ui.add_layers()