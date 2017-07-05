"""Define some meta component of lexer.
"""

token_type = ("KW", "ID", "OP", "DIM", "VAL", "EOF", "INVALID")
keywords = ("if", "else", "then", "case", "while", "do", "break", "continue", "return", "switch")
var_type = ("int", "float", "char", "bool")


class Position(object):

    def __init__(self, line: int, col: int):
        self.line: int = line
        self.col: int = col


class Token(object):
    """
    token is the output of lexer.

    which purpose is to make parse work easier.
    """

    def __init__(self, t_type: str, value: str):
        self.t_type = t_type
        self.value = value

    def match(self):
        pass

    # def _checkType(self, t_type):
    #     if t_type not in token_type:
    #         raise TokenNotSupportError
