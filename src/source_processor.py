"""
this is a tool set for source code process.
"""
from typing import Tuple


class Cursor(object):
    """mark token's position in the source code."""

    def __init__(self, line: int, col: int):
        self.line: int = line
        self.col: int = col

    def get_position(self) -> Tuple[int, int]:
        """return position"""
        return self.line, self.col


class BaseSourceProcessor(object):
    """character peeker."""

    def __init__(self):
        self.position = None

    def pretreatment(self, string):
        """pretreatment the source code"""
        raise NotImplementedError

    def next_char(self) -> str:
        """return next char to process"""
        raise NotImplementedError


class FileSourceProcessor(BaseSourceProcessor):
    """character peeker for files."""

    def __init__(self, file_name):
        super(FileSourceProcessor, self).__init__()
        self.file_obj = open(file_name, 'r')
        self.cursor = Cursor(0, 0)
        self.line_buffer = []

    def pretreatment(self, string) -> str:
        """reduce redundant whitespace and return the str"""
        return ' '.join([ch for ch in string.split(' ') if ch != ''])

    def reload_buffer(self):
        if self.line_buffer:
            self.line_buffer = list(self.pretreatment(self.file_obj.readline()))

    def next_char(self) -> str:
        if self.line_buffer:
            return self.line_buffer.pop(0)
        else:
            self.reload_buffer()
            if self.line_buffer:
                return "λ"
            else:
                return self.line_buffer.pop(0)
