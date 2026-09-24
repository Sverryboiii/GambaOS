from src.gambaos.system.GambaOS.integrated.pyrolang import storage
import sverpykit as spk

# All Built-in methods that are used for PyroLang.
def _add(*values):
    val = storage.Float(values[0])
    for v in values[1:]: val += v
    return val.data

def _subtract(*values):
    val = storage.Float(values[0])
    for v in values[1:]: val -= v
    return val.data

def _multiply(*values):
    val = storage.Float(values[0])
    for v in values[1:]: val *= v
    return val.data

def _divide(*values):
    val = storage.Float(values[0])
    for v in values[1:]: val /= v
    return val.data

def _equals(a, b):
    return a == b

def _avg(*values):
    return _add(*values) / len(values)

def _max(*values):
    highest = values[0]
    for v in values:
        if v.data > highest.data:
            highest = v
    return highest

def _min(*values):
    lowest = values[0]
    for v in values:
        if v.data < lowest.data:
            lowest = v
    return lowest

def is_printable_value(value):
    return isinstance(value, storage.String)\
        or isinstance(value, storage.Integer)\
        or isinstance(value, storage.Float)\
        or isinstance(value, storage.Boolean)

def _out(*values, end=True):
    for val in values:
        if is_printable_value(val):
            storage.storage.text_block.change_text(
                f"{storage.storage.text_block.text}{val.data} "
            )
    if end:
        storage.storage.text_block.change_text(
            f"{storage.storage.text_block.text}\n"
        )

def _in(*values):
    _out(*values, end=False)
    while True:
        spk.run_frame()
        if not storage.storage.input:
            continue
        r = storage.String(storage.storage.input, convert=False)
        storage.storage.input = None
        return r

class Builtins:
    def __init__(self):
        self.methods = {
            "eq": _equals,
            "avg": _avg,
            "max": _max,
            "min": _min,
            "add": _add,
            "sub": _subtract,
            "mult": _multiply,
            "div": _divide,
            "out": _out,
            "in": _in
        }

    def load_builtin(self, name):
        if name not in list(self.methods.keys()):
            raise ValueError(f"Method '{name}' does not exist.")
        storage.storage.functions[name] = self.methods[name]
builtins_ = Builtins()