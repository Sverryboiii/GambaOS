print("Starting GambaOS!")
import pygame, sverpykit as spk
from src.gambaos.system.GambaOS import Ui, Config
pygame.display.set_caption("GambaOS")

spk.set_font()

ui = []
ui.extend(Ui.start_screen)

welcome_text = spk.render_text("Welcome To GambaOS!!!")
def frame():
    spk.draw_surface(welcome_text, (0, 0))
    [part.update() for part in ui]
    [method() for method in Config.frame_functions]

def tick():
    [method() for method in Config.tick_functions]

spk.max_rate(60, 60)

spk.set_frame_method(frame)
spk.set_tick_method(tick)
spk.start()