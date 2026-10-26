from src.gambaos.system.GambaOS.integrated.gml import parser
from src.gambaos.system.GambaOS.integrated.gss import runtime as gss_runtime
from typing import Callable
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


post = []
may_post = False
def execute(code, text_box: spk.TextBlock, window: spk.Window, link_executor, path: str, variables: dict | None = None):
    if not variables:
        variables = {}
    global post, may_post

    parsed_code = parser.parse(code)

    sheet = {}

    def _post(value):
        global post, may_post
        post = value
        may_post = True

    for token in parsed_code:
        text = token["text"]
        tags = token["tags"]

        names = [tag["name"] for tag in tags]

        name = "p"

        if "h" in names:
            name = "h"
        if "POST" in names:
            post.append(text)
            may_post = True

        if "b" in names:
            name += "b"
        if "i" in names:
            name += "i"

        hyperlink = None
        if "link" in names:
            hyperlink = (link_executor, [text])
        if "var" in names:
            text = variables.get(text, "None")
        search_bar = None
        if "input" in names:
            search_bar: tuple[Callable, str] = (_post, text)

        for tag in tags:
            if tag["name"] == "style":
                directory = tag.get("dir", "")
                full_path = os.path.join(path, directory)
                if not directory or not os.path.exists(full_path):
                    raise ValueError(f"No path given or path doesn't exist! Path: {full_path}")
                with open(full_path, "r") as f:
                    code = f.read()
                sheet = gss_runtime.execute(code, window)

        text_color: tuple[int, int, int] | None = sheet.get("text-color", None)
        text_box.add_text(
            f"{text}",
            f"GPP_{name}",
            text_color if text_color else (255, 255, 255),
            hyperlink=hyperlink,
            newline="nl" in names,
            input_=(True, search_bar[0], [], search_bar[1]) if "input" in names else (False, lambda : None, [], "")
        )

    while not may_post:
        spk.run_frame()
    may_post = False
    return post