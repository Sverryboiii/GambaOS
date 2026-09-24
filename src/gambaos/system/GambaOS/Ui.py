import sverpykit as spk, pygame
from src.gambaos.system.GambaOS import Config, FileManager, Runtime

gamba_os_icon = pygame.image.load(FileManager.resource_path("system/GambaOS/GambaOS-icon.png"))

start_screen_button_color = (100, 100, 100)
start_screen_button_rounding = 10

start_screen = [
    spk.Button(
        rect=pygame.Rect(
            -Config.screen.get_width() / 12, Config.screen.get_height() / 40 * 38,
            Config.screen.get_width() / 5, Config.screen.get_height() / 20
        ),
        button_color=(50, 50, 50),
        surface=gamba_os_icon,
        display=Config.screen,
        rounding=int(Config.screen.get_height() / 50),
        function=spk.add_layer,
        layer_type="window",
        rectangle=pygame.Rect(
            0,
            Config.screen.get_height() / 3 * 2,
            Config.screen.get_width() / 5,
            Config.screen.get_height() / 3
        ),
        components=[
            spk.Button(
                rect=pygame.Rect(
                    10, 10,
                    Config.screen.get_width() / 5 - 20,
                    30
                ),
                button_color=start_screen_button_color,
                surface=spk.render_text("SHUT DOWN"),
                display=Config.screen,
                rounding=start_screen_button_rounding,
                function=spk.quit_game
            ),
            spk.Button(
                rect=pygame.Rect(
                    10, 50,
                    Config.screen.get_width() / 5 - 20,
                    30
                ),
                button_color=start_screen_button_color,
                surface=spk.render_text("APPLICATIONS"),
                display=Config.screen,
                rounding=start_screen_button_rounding,
                function=spk.add_layer,
                layer_type="window",
                rectangle=pygame.Rect(
                    Config.screen.get_width() / 2 - Config.screen.get_width() / (5*2),
                    Config.screen.get_height() / 2 - Config.screen.get_height() / (3*2),
                    Config.screen.get_width() / 5,
                    Config.screen.get_height() / 3
                ),
                components=Runtime.get_application_buttons()
            )
        ],
        # title_bar = False
    )
]