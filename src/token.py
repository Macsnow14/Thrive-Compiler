"""Define some meta component of lexer.
"""
from src.source_processor import Cursor


class Token(object):
    """
    token is the output of lexer.

    which purpose is to make parse work easier.
    """

    def __init__(self, t_type: str, value: str, cursor: Cursor):
        self.t_type = t_type
        self.value = value
        self.cursor = cursor
