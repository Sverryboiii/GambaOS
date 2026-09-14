from src.gambaos.system.GambaOS import FileManager
import os, sverpykit as spk

window: spk.Window

def get_files(directory: str):
    return os.listdir(FileManager.resource_path(directory))