from src.gambaos.system.pyrolang import parser
import typing, sverpykit as spk

main_code = None

def tokenize(file, start: int = 0, function=False) -> None | typing.Any:
    with open(file, "r") as f:
        code = f.read()

    lines = code.split("\n")[start:]
    skips = 0

    for count, line in enumerate(lines):
        spk.run_frame()
        line: str = line.strip()
        if line == "":
            continue

        if line.startswith("//"):
            continue

        if line.startswith("{"):
            skips += 1
            continue

        if line.endswith("}"):
            skips -= 1
            if function and skips == -1:
                return
            continue
        elif skips > 0:
            continue

        split_line = line.split(" ")
        remove_empties = 0
        for line in split_line:
            if line.strip() == "":
                remove_empties += 1
        for _ in range(remove_empties):
            split_line.remove("")

        base_command = split_line[0]
        token: dict[str, typing.Any] = {
            "base_command": base_command,
            "function": function,
            "line": count,
            "file": file
        }

        # Get built-in function/method.
        if base_command == "GET":
            token["action"] = split_line[1]
        # Get external .pr file.
        elif base_command == "GETF":
            token["action"] = split_line[1]
        # Set a variable.
        elif base_command == "SET":
            token["action"] = " ".join(split_line[1:])
        # Run 1 function if the expression is true.
        elif base_command == "if":
            token["base_command"] = "IF"
            token["expression"] = split_line[1]
            token["evaluation"] = " ".join(split_line[2:])
        # Create a function.
        elif base_command == "func":
            if not split_line[-1].endswith("{"):
                raise SyntaxError("First line of a function must end on a '{'.")
            token["base_command"] = "FUNC"
            token["name"] = split_line[1]
            token["parameters"] = split_line[2]
            skips += 1
        # Return from a function / Exit the program (Only top level).
        elif base_command == "return":
            value = None if len(split_line) == 1 else " ".join(split_line[1:])
            return parser.parse_value(value, function) if value is not None else None
        # Call a function.
        else:
            token["base_command"] = "FUNCTION"
            token["action"] = base_command
            token["parameters"] = " ".join(split_line[1:])

        parser.parse(token)
    return None