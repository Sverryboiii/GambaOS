from src.gambaos.system.gambapyroprism import parser
import sverpykit as spk, pygame

fonts = {
    "p": ("arial", 20, False, False),
    "pb": ("arial", 20, True, False),
    "pi": ("arial", 20, False, True),
    "pbi": ("arial", 20, True, True),
    "h": ("arial", 40, False, False),
    "hb": ("arial", 40, True, False),
    "hi": ("arial", 40, False, True),
    "hbi": ("arial", 40, True, True)
}

for font_name, font in fonts.items():
    spk.set_font(f"GPP_{font_name}", *font)

def execute(code, text_box: spk.TextBlock, link_executor):

    parsed_code = parser.parse(code)
    print(parsed_code)

    for token in parsed_code:
        text = token["text"]
        tags = token["tags"]

        names = [tag["name"] for tag in tags]

        name = "p"

        if "h" in names:
            name = "h"

        if "b" in names:
            name += "b"
        if "i" in names:
            name += "i"

        hyperlink = None
        if "link" in names:
            hyperlink = (link_executor, [text])

        text_box.add_text(f"{text}", f"GPP_{name}", (255, 255, 255), hyperlink=hyperlink, newline="nl" in names)