from src.gambaos.system.GambaOS.integrated.pyrolang import runtime, storage, Builtins

number_operations = "<>-+*/"
operations = "<>=|"
value_extensions = "!+-B"

def parse_value(value, function: storage.Function):
    value = value.strip()
    if value.endswith('"!'):
        return storage.String(value)
    if value.endswith('"+'):
        return storage.Integer(value)
    if value.endswith('"-'):
        return storage.Float(value)
    if value.endswith('"B'):
        return storage.Boolean(value)
    if function and value in function.scope.keys():
        return function.scope[value]
    print(storage.storage.file, storage.storage.active_file)
    if value in (
            storage.storage.variables.keys() if storage.storage.file == storage.storage.active_file
        else storage.storage.scopes[storage.storage.active_file].keys()
    ):
        if storage.storage.file == storage.storage.active_file:
            return storage.storage.variables[value]
        else:
            return storage.storage.scopes[storage.storage.active_file][value]
    print(storage.storage.variables, value)
    raise ValueError(f"Unrecognized data-type '{value[-1]}' in {value}.")

def parse_expression(expression: str, function: storage.Function) -> bool:

    token = []

    last_count = 0
    for c, char in enumerate(expression):
        if char not in operations:
            continue
        token.append(expression[last_count:c])
        token.append(char)
        last_count = c+1
    token.append(expression[last_count:])


    # print(token)
    for c, key in enumerate(token):

        if key not in operations:
            continue

        last_value = parse_value(token[c-1], function)
        next_value = parse_value(token[c+1], function)

        if key in number_operations and (not (
                isinstance(last_value, storage.Integer) or
                isinstance(last_value, storage.Float)
        ) or not (
                isinstance(next_value, storage.Integer) or
                isinstance(next_value, storage.Float)
        )):
            raise TypeError(f"Invalid data type(s) for operator '{key}'.")

        print(last_value.data, next_value.data, key, last_value.data == next_value.data, type(last_value .data), type(next_value.data))
        if key == "=" and last_value.data != next_value.data:
            return False
        if key == "|" and last_value.data == next_value.data:
            return False
        if key == ">" and last_value.data <= next_value.data:
            return False
        if key == "<" and last_value.data >= next_value.data:
            return False
    return True

def parse_parameters(parameters: str, function: storage.Function):
    save = None
    parameters = parameters.strip()[1:].split(";")
    if not parameters[-1].strip().endswith(")"):
        function_end = parameters[-1].rfind(") -> ")
        save = parameters[-1][function_end+5:]
        parameters[-1] = parameters[-1][:function_end]
    else:
        parameters[-1] = parameters[-1][:-1]

    if parameters == [""]:
        return {
            "values": [],
            "save": save
        }
    values = []

    # Change values to their own class.
    for parameter in parameters:
        values.append(parse_value(parameter, function))

    return {
        "values": values,
        "save": save
    }

def parse(token: dict):
    # print(token)

    func = lambda : None
    values = []
    save: str | None = None

    if token["base_command"] == "GET":
        func = Builtins.builtins_.load_builtin
        values = [token["action"]]
    elif token["base_command"] == "GETF":
        func = storage.storage.load_file
        values =  [token["action"]]
    elif token["base_command"] == "SET":
        func = storage.storage.add_variable
        split_action = token["action"].strip().split(" ")
        values = [split_action[0], parse_value(split_action[1], token["function"])]
    elif token["base_command"] == "IF":
        expression = token["expression"].strip()
        if not (expression.startswith("[") and expression.endswith("]")):
            return
        expression = expression[1:-1]
        true = parse_expression(expression, token["function"])
        evaluations = token["evaluation"].strip() # _fun ("_\"!)_ _fun ()_
        split_evaluations = []
        start_eval = False
        in_value = False
        function_over = True
        ignore_next = False
        for c, char in enumerate(evaluations):
            if ignore_next:
                ignore_next = False
                continue
            if char == "_" and not in_value and function_over:
                start_eval = not start_eval
                function_over = False
                if not start_eval:
                    split_evaluations.append(evaluations[:c+1])
                    split_evaluations.append(evaluations[c+1:])
                    break
            if char == '"':
                if in_value:
                    if evaluations[c+1] in value_extensions:
                        in_value = False
                else:
                    in_value = True
            if char == "\\" and in_value:
                ignore_next = True
            if char == ")":
                function_over = True
        evaluation = split_evaluations[0 if true else 1].strip()
        if not (evaluation.startswith("_") and evaluation.endswith("_")):
            raise SyntaxError("Evaluations must start and end with '_'.")
        evaluation = evaluation[1:-1].split(' ')
        name = evaluation[0]
        arguments = " ".join(evaluation[1:])
        payload = parse_parameters(arguments, token["function"])
        func = storage.storage.functions[name]
        save = payload["save"]
        values = payload["values"]
    elif token["base_command"] == "FUNC": # Creation
        func = storage.storage.add_pr_function
        parameters = token["parameters"]
        if not parameters.startswith("[") or not parameters.endswith("]"):
            raise SyntaxError ("Parameters must start with '[' and end with ']'.")
        parameters = parameters[1:-1].split(";") if len(parameters[1:-1]) > 0 else []
        values = [token["name"], token["line"], token["file"], parameters]
    elif token["base_command"] == "FUNCTION": # Calling
        func = storage.storage.functions[token["action"]]
        payload = parse_parameters(token["parameters"], token["function"])
        save = payload["save"]
        values = payload["values"]

    if isinstance(func, storage.Function):
        func = func.run

    runtime.run(func, *values, save=save)