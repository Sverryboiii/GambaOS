from src.gambaos.system.GambaOS.integrated.pyrolang import storage


def run(func, *values, save: str | None = None):
    val = func(*values)
    if save:
        if isinstance(val, storage.Integer) or\
                isinstance(val, storage.String) or\
                isinstance(val, storage.Float) or\
                isinstance(val, storage.Boolean):
            storage.storage.add_variable(save, val)
    # print(storage.storage.variables)