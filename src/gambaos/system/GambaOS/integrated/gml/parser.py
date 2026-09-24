
class GppError(Exception):
    """This is an error for GambaPyroPrism."""

def parse_tag(tag) -> tuple[dict, bool]:

    parsed_tag = {}
    remove: bool = tag[1] == "/"
    if remove: tag = tag[1:]

    new_tag = tag[1:-1]
    if not ":" in new_tag:
        parsed_tag["name"] = new_tag
        return parsed_tag, remove

    tag_name = new_tag.split(":")[0]
    unparsed_parameters = ":".join(new_tag.split(":")[1:])

    parsed_tag["name"] = tag_name

    for param in unparsed_parameters.split(";"):
        var = param.split("=")[0].strip()
        val = param.split("=")[1].strip()
        parsed_tag[var] = val

    return parsed_tag, remove

def parse(text) -> list:

    text = "".join(text.split("\n"))

    if not text.startswith("<GML>"):
        raise GppError("File must start with '<GML>' to initialize that it's a GPP file!")
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