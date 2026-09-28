from src.gambaos.system.GambaOS import FileManager, Config
import sverpykit as spk, pygame

file_data = ""
cursor_position = (0,0)
cursor = spk.render_text("|", color=(25, 25, 25), name="tiny")

window: spk.Window
text_box: spk.TextBlock

def save(file, data):
    relative_path = FileManager.resource_path(file)
    with open(relative_path, "w") as f:
        f.write(data)

def tick():
    global cursor_position, file_data

    for event in spk.Config.events:
        if event.type != pygame.KEYDOWN:
            continue
        if event.key == pygame.K_BACKSPACE:
            pass
        elif event.key == pygame.K_RETURN:
            pass
        elif event.key == pygame.K_RIGHT:
            pass
        elif event.key == pygame.K_LEFT:
            new_x = cursor_position[0] - 1
            new_y = cursor_position[1]
            if new_x < 0:
                new_y = max(0, cursor_position[1] - 1)
                new_x = len(file_data.split("\n")[new_y])
            cursor_position = (new_x, new_y)
        elif event.unicode.isprintable():
            pass

def open_file(file_path):
    global file_data

    relative_path = FileManager.resource_path("user/"+file_path)
    with open(relative_path, "r") as f:
        file_data = f.read()

    text_box.reset()
    for line in file_data.split("\n"):
        text_box.add_text(line, "tiny", (25, 25, 25), newline=True)
    Config.tick_functions.append(tick)
    Config.frame_functions.append(frame)