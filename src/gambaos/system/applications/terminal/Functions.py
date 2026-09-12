from src.gambaos.system.pyrolang import execute as exe, storage
from src.gambaos.system.GambaOS.FileManager import resource_path
import sverpykit as spk, pygame

input_bar: spk.SearchBar
text_box: spk.TextBlock

running_program: bool = False
program_storage: storage.Storage = storage.Storage(spk.TextBlock(pygame.Rect(0, 0, 0, 0), "out of use"))

def execute(operation: str):
    global program_storage

    text_box.change_text(
        f"{text_box.text}{operation}\n"
    )

    split_operation = operation.split(" ")
    if running_program:
        program_storage.input = operation
        text_box.change_text(f"{text_box.text}{operation}")
    elif split_operation[0] in commands:
        if len(split_operation) > 1:
            commands[split_operation[0]](*split_operation[1:])
        else:
            commands[split_operation[0]]()
    else:
        text_box.change_text(
            f"{text_box.text}[Error] >> "
            f"Command '{split_operation[0]}' not found!\n"
        )

    text_box.change_text(
        f"{text_box.text}\n>> "
    )

def clear_screen():
    text_box.change_text(">> ")

def run_pyrolang_script(file: str):
    global program_storage, running_program
    input_bar.stored = ""
    running_program = True
    storage.storage = storage.Storage(text_box)
    program_storage = storage.Storage
    exe.execute(resource_path(f"user/{file}"))
    input_bar.function = execute
    running_program = False

commands = {
    "cls": clear_screen,
    "pyro": run_pyrolang_script
}