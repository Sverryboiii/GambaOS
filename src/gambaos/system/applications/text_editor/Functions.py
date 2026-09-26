from src.gambaos.system.GambaOS import FileManager
import sverpykit as spk

file_data = ""
window: spk.Window
text_box: spk.TextBlock

def save(file, data):
    relative_path = FileManager.resource_path(file)
    with open(relative_path, "w") as f:
        f.write(data)

def open_file(file_path):
    global file_data

    relative_path = FileManager.resource_path("user/"+file_path)
    with open(relative_path, "r") as f:
        file_data = f.read()

    text_box.reset()
    for line in file_data.split("\n"):
        text_box.add_text(line, "tiny", (25, 25, 25), newline=True)