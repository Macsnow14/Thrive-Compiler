"""Define some meta component of lexer.
"""
from typing import List
from src.source import Cursor


class Token(object):
    """
    token is the output of lexer.

    which purpose is to make parse work easier.
    """

    def __init__(self, t_type: str, value: str or bool or int, cursor: Cursor):
        self.type: str = t_type
        self.value: str or bool or int = value
        self.cursor: Cursor = cursor

    def __str__(self):
        return '("%s", %s)' % (self.value, self.type)

    def __repr__(self):
        return '("%s", %s)' % (self.value, self.type)


class TokenSource(object):
    """
    processed source.
    basiclly its a list of token with handle method.
    """

    def __init__(self, token_list: List[Token]):
        self.token_list: List[Token] = token_list
        self.source_len = len(self.token_list)
        self.token_pointer: int = 0

    def get(self):
        self.token_pointer += 1
        return self.token_list[self.token_pointer - 1]

    def peek(self, seq: int=1):
        if self.token_pointer + seq - 1 >= self.source_len:
            return Token("EOF", -1, Cursor(-1, -1))
        return self.token_list[self.token_pointer + seq - 1]
