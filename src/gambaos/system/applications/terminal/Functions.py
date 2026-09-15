from src.gambaos.system.GambaOS.integrated.pyrolang import execute as exe, storage
from src.gambaos.system.GambaOS.FileManager import resource_path
import sverpykit as spk, pygame, os, shutil

window: spk.Window

input_bar: spk.SearchBar
text_box: spk.TextBlock

running_program: bool = False
program_storage: storage.Storage = storage.Storage(spk.TextBlock(pygame.Rect(0, 0, 0, 0), "out of use"))

current_directory = "user"

def error_message(message):
    text_box.add_text(
        f"[Error] >> {message}",
        "tiny", color=(255, 255, 255), newline=True
    )

def execute(operation: str):
    global program_storage

    text_box.add_text(
        f"{operation}",
        "tiny", color=(255, 255, 255), newline=True
    )

    split_operation = operation.split(" ")
    if running_program:
        program_storage.input = operation
        text_box.add_text(
            f"{operation}",
            "tiny", color=(255, 255, 255)
        )
    elif split_operation[0] in commands:
        try:
            if len(split_operation) > 1:
                commands[split_operation[0]](*split_operation[1:])
            else:
                commands[split_operation[0]]()
        except TypeError:
            error_message("Too little or too many arguments are given!")
    else:
        text_box.add_text(
            f"[Error] >> Command '{split_operation[0]}' not found!",
            "tiny", color=(255, 255, 255), newline=True
        )

    text_box.add_text(
        f"GambaOS/{current_directory} >> ",
        "tiny", color=(255, 255, 255), newline=False
    )

def clear_screen():
    text_box.text = ""
    text_box.text_surfs = []

def make_directory(directory: str):
    os.makedirs(resource_path(os.path.join(current_directory, directory)))

def delete_directory(directory: str):
    shutil.rmtree(resource_path(os.path.join(current_directory, directory)))

def make_file(directory: str):
    with open(resource_path(os.path.join(current_directory, directory)), "w") as f:
        f.write("")

def delete_file(directory: str):
    os.remove(resource_path(os.path.join(current_directory, directory)))

def change_directory(directory):
    global current_directory
    new_directory = current_directory
    for part in directory.split("/"):
        if part != "..":
            new_directory = os.path.join(new_directory, part)
            continue
        new_directory = "/".join(new_directory.split("/")[:-1])
    if os.path.exists(resource_path(new_directory)):
        current_directory = new_directory
        return
    error_message(f"Directory {new_directory} does not exist!")

def show_directory(directory=""):
    for c, path in enumerate(os.listdir(resource_path(os.path.join(current_directory, directory)))):
        if (c+1) % 3 == 0:
            text_box.add_text(
                f"{text_box.text}{path}\n",
                "tiny", color=(255, 255, 255), newline=True
            )
        else:
            text_box.add_text(
                f"{text_box.text}{path}   ",
                "tiny", color=(255, 255, 255), newline=False
            )

def run_pyrolang_script(file: str):
    global program_storage, running_program
    input_bar.stored = ""
    running_program = True
    storage.storage = storage.Storage(text_box)
    program_storage = storage.Storage
    exe.execute(resource_path(f"user/{file}"))
    input_bar.function = execute
    running_program = False

def hyperlink(text, *action):
    text_box.add_text(text, "tiny", (255, 255, 255), (execute, action), newline=True)

def exit_terminal():
    window.close()

commands = {
    "cls": clear_screen,
    "pyro": run_pyrolang_script,
    "mkdir": make_directory,
    "mkfile": make_file,
    "rmdir": delete_directory,
    "rmfile": delete_file,
    "dir": show_directory,
    "cd": change_directory,
    "hyperlink": hyperlink,
    "exit": exit_terminal
}