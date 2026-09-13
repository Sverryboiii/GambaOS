import pygame, sverpykit as spk
import src.gambaos.system.GambaOS.Ui as Ui
pygame.display.set_caption("GambaOS")

spk.set_font()

ui = []
ui.extend(Ui.start_screen)

welcome_text = spk.render_text("Welcome To GambaOS!!!")
def frame():
    spk.draw_surface(welcome_text, (0, 0))
    [part.update() for part in ui]

spk.max_rate(60, 60)

spk.set_frame_method(frame)
spk.start()