from src.gambaos.system.GambaOS.integrated.pyrolang import lexer, storage

def execute(path: str) -> None:
    print("Executing:", path)
    storage.storage.file = "/".join(path.split("/")[:-1])
    lexer.main_code = path
    lexer.tokenize(path)

# execute("main.pr")