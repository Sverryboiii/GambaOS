from src.gambaos.system.GambaOS.FileManager import resource_path
import sverpykit as spk

class Boolean:
    def __init__(self, boolean: str | bool):
        self.data = boolean # "True"=
        if isinstance(self.data, str):
            self.convert()

    @staticmethod
    def is_bool(value: str):
        return value.startswith('"') and value.endswith('"=')

    def convert(self):
        boolean = self.data[1:].split('"')[0]
        self.data = boolean == "true" or boolean == "True"

class Float:
    def __init__(self, float_: str | float):
        self.data = float_ # "4.0"-
        if isinstance(self.data, str):
            self.convert()

    @staticmethod
    def is_float(value: str) -> bool:
        return value.startswith('"') and value.endswith('"-')

    def __add__(self, other):
        return Float(self.data + other.data)

    def __sub__(self, other):
        return Float(self.data - other.data)

    def __mul__(self, other):
        return Float(self.data * other.data)

    def __truediv__(self, other):
        if isinstance(other, Integer) or\
                isinstance(other, Float):
            return Float(self.data / other.data)
        return Float(self.data / other)

    def __eq__(self, value: object, /) -> bool:
        return self.data == value.data

    def __lt__(self, other):
        return self.data < other.data

    def __gt__(self, other):
        return self.data > other.data

    def convert(self):
        float_ = self.data[1:]
        self.data = float(float_.split('"')[0])

class Integer:
    def __init__(self, integer: str | int):
        self.data = integer # "4"+
        if isinstance(self.data, str):
            self.convert()

    @staticmethod
    def is_int(value: str):
        return value.startswith('"') and value.endswith('"+')

    def __add__(self, other):
        if isinstance(other, Integer):
            return Integer(self.data + other.data)
        if isinstance(other, Float):
            return Float(self.data + other.data)
        return Integer(self.data + other)

    def __sub__(self, other):
        if isinstance(other, Integer):
            return Integer(self.data - other.data)
        if isinstance(other, Float):
            return Float(self.data - other.data)
        return Integer(self.data - other)

    def __truediv__(self, other):
        if isinstance(other, Integer) or\
                isinstance(other, Float):
            return Float(self.data / other.data)
        return Float(self.data / other)

    def __mul__(self, other):
        if isinstance(other, Integer):
            return Integer(self.data * other.data)
        if isinstance(other, Float):
            return Float(self.data * other.data)
        return Integer(self.data * other)

    def __eq__(self, value) -> Boolean:
        if isinstance(value, Integer) or\
                isinstance(value, Float):
            return Boolean(self.data == value.data)
        return Boolean(self.data == value)

    def __lt__(self, other):
        if isinstance(other, Integer) or\
                isinstance(other, Float):
            return self.data < other.data
        return self.data < other

    def __gt__(self, other):
        if isinstance(other, Integer) or\
                isinstance(other, Float):
            return self.data > other.data
        return self.data > other

    def convert(self):
        integer = self.data[1:]
        self.data = int(integer.split('"')[0])

class String:
    def __init__(self, string: str, convert=True):
        self.data = string # "abc123"!
        if convert:
            self.convert()

    @staticmethod
    def is_str(value: str):
        return value.startswith('"') and value.endswith('"!')

    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, String):
            return self.data == value.data
        return self.data == value

    def convert(self):
        string = self.data[1:]
        self.data = str(string.split('"')[0])

# FIX: Make the import at the top of the file.
class Function:
    def __init__(self, start, file, parameters):
        self.start = start+1
        self.file = file
        self.parameters = parameters

        self.scope = {}

    def run(self, *arguments):
        from src.gambaos.system.GambaOS.integrated.pyrolang import lexer
        if len(self.parameters) != len(arguments):
            raise TypeError(f"This function accepts '{len(self.parameters)}', but you gave '{len(arguments)}'.")
        for count, parameter in enumerate(self.parameters):
            self.scope[parameter] = arguments[count]
        val = lexer.tokenize(self.file, self.start, function=self)
        return val


class Storage:
    def __init__(self, text_block):
        self.variables = {}
        self.functions = {}

        self.text_block: spk.TextBlock = text_block
        self.input = None

    def add_variable(self, var, val):
        self.variables[var] = val

    def add_pr_function(self, name, start, file, parameters):
        self.functions[name] = Function(start, file, parameters)

    @ staticmethod
    def load_file(directory: str):
        from src.gambaos.system.GambaOS.integrated.pyrolang import lexer
        lexer.tokenize(resource_path(f"system/pyrolang/{directory}"))
storage: Storage