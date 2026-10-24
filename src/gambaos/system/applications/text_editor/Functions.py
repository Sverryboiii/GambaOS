from src.gambaos.system.GambaOS import FileManager, Config
import sverpykit as spk, pygame

file_data = ""
full_file_path = ""
window: spk.Window
text_box: spk.TextBlock

def close():
    print("Closing text editor...")
    Config.tick_functions.remove(tick)
    window.owner.remove(window)

def init_close():

    window.close = close

    window.operational_buttons = [
        spk.Button(
            rect=pygame.Rect(
                window.rect.x + window.rect.w - window.title_bar_rect.h * 2,
                window.rect.y - window.title_bar_rect.h,
                window.title_bar_rect.h,
                window.title_bar_rect.h
            ),
            button_color=(50, 50, 50),
            surface=spk.render_text("-"),
            display=Config.screen,
            rounding=int(window.title_bar_rect.h / 3),
            function=window.minimize
        ),
        spk.Button(
            rect=pygame.Rect(
                window.rect.x + window.rect.w - window.title_bar_rect.h,
                window.rect.y - window.title_bar_rect.h,
                window.title_bar_rect.h,
                window.title_bar_rect.h
            ),
            button_color=(50, 50, 50),
            surface=spk.render_text("x"),
            display=Config.screen,
            rounding=int(window.title_bar_rect.h / 3),
            function=window.close
        )
    ]

def tick():

    if spk.Runtime.ui_layers[-1] != window:
        return

    global file_data
    updated = False
    keys = pygame.key.get_pressed()
    for event in spk.Config.events:
        if event.type != pygame.KEYDOWN:
            continue
        if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
            if event.key == pygame.K_s:
                save_file()
                continue
        elif event.key == pygame.K_BACKSPACE:
            file_data = file_data[:-1]
        elif event.key == pygame.K_RETURN:
            file_data = file_data = "\n"
        elif event.unicode.isprintable() and len(event.unicode) == 1:
            file_data = file_data + event.unicode
        updated = True

    if updated:
        text_box.reset()
        for line in file_data.split("\n"):
            text_box.add_text(line, "tiny", (25, 25, 25), newline=True)

def save_file():
    global file_data, full_file_path
    with open(full_file_path, "w") as f:
        f.write(file_data)
    print("Saved data!")

def open_file(file_path):
    global file_data, full_file_path

    full_file_path = FileManager.resource_path("user/"+file_path)
    with open(full_file_path, "r") as f:
        file_data = f.read()

    text_box.reset()
    for line in file_data.split("\n"):
        text_box.add_text(line, "tiny", (25, 25, 25), newline=True)
    Config.tick_functions.append(tick)

    init_close()