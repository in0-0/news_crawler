from parser.cnbc import ParserCNBC
from parser.naver import ParserNaver
from parser.defualt_parser import DefualtParser
from parser.yahoo import ParserYahoo

PB_YAHOO = "yahoo"
PB_NAVER = "naver"
PB_CNBC = "cnbc"


class ParserFactory:

    @staticmethod
    def get_parser(publisher):
        if publisher == PB_NAVER:
            return ParserNaver()
        if publisher == PB_YAHOO:
            return ParserYahoo()
        if publisher == PB_CNBC:
            return ParserCNBC()

        return DefualtParser()
