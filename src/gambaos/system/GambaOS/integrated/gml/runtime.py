from src.gambaos.system.GambaOS.integrated.gml import parser
from src.gambaos.system.GambaOS.integrated.gss import runtime as gss_runtime
import sverpykit as spk, os

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

def execute(code, text_box: spk.TextBlock, window: spk.Window, link_executor, path: str):

    parsed_code = parser.parse(code)

    sheet = {}
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

        for tag in tags:
            if tag["name"] == "style":
                directory = tag.get("dir", "")
                full_path = os.path.join(path, directory)
                if not directory or not os.path.exists(full_path):
                    raise ValueError("No path given or path doesn't exist!")
                with open(full_path, "r") as f:
                    code = f.read()
                sheet = gss_runtime.execute(code, window)

        text_color: tuple[int, int, int] | None = sheet.get("text-color", None)
        text_box.add_text(
            f"{text}",
            f"GPP_{name}",
            text_color if text_color else (255, 255, 255),
            hyperlink=hyperlink,
            newline="nl" in names
        )