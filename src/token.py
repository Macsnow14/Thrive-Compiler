"""Define some meta component of lexer.
"""

token_type = ("KW", "ID", "OP", "DIM", "VAL", "EOF", "INVALID")


class Token(object):
    """
    token is the output of lexer.

    which purpose is to make parse work easier.
    """

    def __init__(self, t_type: str, value: str, position: int):

        self.t_type = t_type
        self.value = value
        self.position = position

    def match(self):
        pass

    # def _checkType(self, t_type):
    #     if t_type not in token_type:
    #         raise TokenNotSupportError
