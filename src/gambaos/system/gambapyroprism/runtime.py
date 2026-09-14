from src.gambaos.system.gambapyroprism import parser
import sverpykit as spk

def execute(code, text_box: spk.TextBlock):

    parsed_code = parser.parse(code)

    for token in parsed_code:
        text = token["text"]
        tags = token["tags"]