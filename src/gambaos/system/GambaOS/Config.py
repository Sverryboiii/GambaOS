import screeninfo, pygame, sverpykit as spk, os

monitors = screeninfo.get_monitors()
primary_monitor = None
for monitor in monitors:
    if monitor.is_primary:
        primary_monitor = monitor
if not primary_monitor:
    primary_monitor = monitors[0]

spk.set_font("tiny", "arial", 18)

os.environ['SDL_VIDEO_CENTERED'] = '1'
screen = spk.set_display(primary_monitor.width, primary_monitor.height, pygame.FULLSCREEN)
font = spk.set_font()