
class GppError(Exception):
    """This is an error for GambaPyroPrism."""

def parse_tag(tag) -> tuple[dict, bool]:

    parsed_tag = {}
    remove: bool = tag[1] == "/"
    if remove: tag = tag[1:]

    split_tag = tag.split(" ")

    parsed_tag["name"] = split_tag[0][1:-1]

    return parsed_tag, remove

def parse(text) -> list:

    text = "".join(text.split("\n"))

    if not text.startswith("<GPP>"):
        raise GppError("File must start with '<GPP>' to initialize that it's a GPP file!")
    text = text[5:]

    parsed_text = [{"text": "", "tags": []}]

    layer = []

    in_tag = False
    for c, char in enumerate(text):
        if char == ">" and in_tag:
            in_tag = False
        elif char == "<":
            in_tag = True
            tag = text[c:].split(">")[0] + ">"
            parsed_tag = parse_tag(tag)
            if parsed_tag[0]["name"] == "l":
                parsed_text[-1]["tags"] = layer.copy()
                layer = []
                parsed_text.append({"text": "", "tags": []})
                continue
            if parsed_tag[1] and parsed_tag[0] in parsed_text[-1]["tags"]:
                layer.remove(parsed_tag[0])
            else:
                layer.append(parsed_tag[0])
        elif not in_tag:
            parsed_text[-1]["text"] += char
    if layer != []:
        parsed_text[-1]["tags"] = layer.copy()

    return parsed_text