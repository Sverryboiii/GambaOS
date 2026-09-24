import math

hex_to_dec = {}
for c, char in enumerate("0123456789abcdef"):
    hex_to_dec[char] = c

def parse_hex(hex_or_dec) -> str | int:
    if not hex_or_dec.startswith("#"):
        return hex(hex_or_dec)

    hex_ = hex_or_dec[1:].lower()
    value = 0

    for c, char in enumerate(reversed(hex_)):
        value += hex_to_dec[char] * math.pow(16, c)
    return value

def parse(code):

    code = "".join(code.strip().split("\n"))

    if not code.startswith("{") and code.endswith("}"):
        raise SyntaxError("GSS files must be withing curly brackets '{}'.")

    code = code[1:-1]

    sheet = {}

    for line in code.split(";"):
        # Every line states what something could do with a "=" mark.
        if line.strip() == "":
            continue

        split_line = line.split("=")

        obj = split_line[0].strip()
        val = "=".join(split_line[1:]).strip()

        if "color" in obj:
            if val.startswith("#"):
                r = parse_hex("#" + val[1:3])
                g = parse_hex("#" + val[3:5])
                b = parse_hex("#" + val[5:7])
                val = (r, g, b)
            else:
                pass

        sheet[obj] = val

    return sheet