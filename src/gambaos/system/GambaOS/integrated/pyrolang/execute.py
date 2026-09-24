from src.gambaos.system.GambaOS.integrated.pyrolang import lexer


def execute(code: str) -> None:
    lexer.main_code = code
    lexer.tokenize(code)

# execute("main.pr")