from src.gambaos.system.GambaOS.integrated.pyrolang import storage
from src.gambaos.system.GambaOS.integrated.gml import runtime as run_gml
from src.gambaos.system.GambaOS import FileManager
from src.gambaos.system.applications.web_explorer import Config as WebConfig
import sverpykit as spk, time, os, json
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
    if "address" in storage.storage.customs.keys():
        print(*[val.data for val in values])
        return
    for c, val in enumerate(values):
        if is_printable_value(val):
            storage.storage.text_block.add_text(
                text=f"{val.data}",
                font=storage.storage.text_block.font,
                color=spk.Config.BEIGE,
                newline=newline and c+1 == len(values)
            )

    post = []
    may_post = False

def _in(*values):
    _out(*values, newline=False)
    r = ""
    while True:
        spk.run_frame()
        if not storage.storage.input:
            continue
        r = storage.storage.input
        storage.storage.input = None
        break
    return storage.String(r, convert=False)

def _exit():
    storage.storage.terminate = True

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

def _gml(path, *variables):
    """
    :param path:
    :param variables:
    Format: [var, val, var, val ...]
    :return:
    """
    new_vars = {}
    for c, val in enumerate(variables):
        if c % 2 != 0:
            continue
        new_vars[val.data] = variables[c+1].data
    with open(FileManager.project_level_path(f"external_servers/{path.data}"), "r") as f:
        data = f.read()

    storage.storage.customs["window"].components = [
        component for component in storage.storage.customs["window"].components if not isinstance(component, spk.Button)
    ]
    storage.storage.customs["window"].color = WebConfig.window_color
    storage.storage.text_block.text_surfs = []
    storage.storage.text_block.searchbars = []
    storage.storage.text_block.text = ""

    return storage.String(str(run_gml.execute(
        data,
        storage.storage.text_block,
        storage.storage.customs["window"],
        storage.storage.customs["link_executor"],
        storage.storage.customs["address"],
        new_vars
    )), convert=False)

def _read(file):
    full_path = os.path.join(storage.storage.file, file.data)
    with open(full_path, "r") as f:
        return storage.String(f.read(), convert=False)

def _write(file, data):
    full_path = os.path.join(storage.storage.file, file.data)
    with open(full_path, "w") as f:
        f.write(data.data)

def _json_pack(obj, var, val, autodict = storage.Boolean(True)):
    obj = json.loads(obj.data)
    try:
        obj[var.data] = json.loads(val.data) if autodict.data else val.data
    except json.decoder.JSONDecodeError:
        obj[var.data] = val.data
    except TypeError:
        obj[var.data] = val.data
    obj = json.dumps(obj)
    return storage.String(obj, convert=False)

def _json_upack(obj, var):
    if not isinstance(obj.data, dict):
        obj = json.loads(obj.data)
    else:
        obj = obj.data
    val = obj.get(var.data)
    print(val)
    if not val:
        return storage.Boolean(False)
    return storage.String(str(val).replace("'", '"'), convert=False) if isinstance(val, str) or isinstance(val, list) or isinstance(val, dict)\
        else storage.Integer(val) if isinstance(val, int)\
        else storage.Float(val) if isinstance(val, float)\
        else storage.Boolean(val) if isinstance(val, bool) else storage.Boolean(False)

def _to_s(val):
    return storage.String(str(val.data), convert=False)

def _type(val):
    return storage.String(str(type(val)), convert=False)

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
            "exit": _exit,
            "time": _time,
            "gml": _gml,
            "read": _read,
            "write": _write,
            "json_pack": _json_pack,
            "json_upack": _json_upack,
            "to_s": _to_s,
            "type": _type
        }

    def load_builtin(self, name):
        if name not in list(self.methods.keys()):
            raise ValueError(f"Method '{name}' does not exist.")
        storage.storage.functions[name] = self.methods[name]
builtins_ = Builtins()