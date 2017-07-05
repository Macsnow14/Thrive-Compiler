"""Define some meta component of lexer.
"""
from src.source_processor import Cursor


class Token(object):
    """
    token is the output of lexer.

    which purpose is to make parse work easier.
    """

    def __init__(self, t_type: str, value, cursor: Cursor):
        self.t_type = t_type
        self.value = value
        self.cursor = cursor

    def __str__(self):
        return '("%s", %s)' % (self.value, self.t_type)

    def __repr__(self):
        return '("%s", %s)' % (self.value, self.t_type)
