from src.gambaos.system.GambaOS.integrated.pyrolang import storage
from src.gambaos.system.GambaOS.integrated.gml import runtime as run_gml
from src.gambaos.system.GambaOS import FileManager
import sverpykit as spk, time
from datetime import datetime

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

def _out(*values, newline=True):
    for c, val in enumerate(values):
        if is_printable_value(val):
            storage.storage.text_block.add_text(
                text=f"{val.data}",
                font=storage.storage.text_block.font,
                color=spk.Config.BEIGE,
                newline=newline and c+1 == len(values)
            )

def _in(*values):
    _out(*values, newline=False)
    r = storage.String("", convert=False)
    while True:
        spk.run_frame()
        if not storage.storage.input:
            continue
        r = storage.String(storage.storage.input, convert=False)
        storage.storage.input = None
        break
    return r

def _time(format_=storage.String("%t", convert=False)):
    """
    :param format_:
    %t = time.time() (seconds since the Unix Epoch)
    %Y = Time in years.
    %M = Time in month of the year (numeric).
    %D = Time in day of the month.
    %f = Time displayed with all needed information.
    :return:
    """

    format_ = format_.data

    # Parse format
    for c, char in enumerate(format_):
        if char != "%":
            continue

        char = format_[c+1]

        if char == "t":
            return storage.Float(time.time())
        if char == "M":
            format_ = format_[:c+1] + "m" + format_[c+2:]
        if char == "D":
            format_ = format_[:c+1] + "d" + format_[c+2:]
        if char == "f":
            format_ = format_[:c+1] + "c" + format_[c+2:]

    return storage.String(datetime.now().strftime(format_), convert=False)

def _gml(path):
    with open(FileManager.project_level_path(f"external_servers/{path.data}"), "r") as f:
        data = f.read()
    run_gml.execute(
        data,
        storage.storage.text_block,
        storage.storage.customs["window"],
        storage.storage.customs["link_executor"],
        storage.storage.customs["address"]
    )

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
            "in": _in,
            "time": _time,
            "gml": _gml
        }

    def load_builtin(self, name):
        if name not in list(self.methods.keys()):
            raise ValueError(f"Method '{name}' does not exist.")
        storage.storage.functions[name] = self.methods[name]
builtins_ = Builtins()