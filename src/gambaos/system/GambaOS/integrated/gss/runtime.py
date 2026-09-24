from src.gambaos.system.GambaOS.integrated.gss import parser
import sverpykit as spk

def execute(code, window: spk.Window):

    parsed_code = parser.parse(code)

    if parsed_code.get("background-color", False):
        window.color = parsed_code["background-color"]

    return parsed_code