"""
this is a tool set for source code process.
"""
from typing import Tuple, List, IO


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

    def is_line_end(self, ch):
        if ch == '\n':
            return True
        else:
            return False

    def next_char(self, peep=False) -> str:
        """return next char to process"""
        raise NotImplementedError


class FileSourceProcessor(BaseSourceProcessor):
    """character peeker for files."""

    def __init__(self, file_name: str):
        super(FileSourceProcessor, self).__init__()
        self.file_obj: IO = open(file_name, 'r')
        self.cursor: Cursor = Cursor(0, 0)
        self.line_buffer: List[str] = []

    def pretreatment(self, string: str) -> str:
        """reduce redundant whitespace and return the str"""
        string: str = string.replace('\t', '').replace('\r', '')
        return ' '.join([ch for ch in string.split(' ') if ch != ''])

    def reload_buffer(self):
        if not self.line_buffer:
            self.line_buffer = list(self.pretreatment(self.file_obj.readline()))

    def next_char(self, peep=False) -> str:
        if self.line_buffer:
            self.cursor.col += 1 if not peep else 0
            return self.line_buffer.pop(0) if not peep else self.line_buffer[0]
        else:
            self.reload_buffer()
            if self.line_buffer:
                self.cursor.line += 1 if not peep else 0
                return self.line_buffer.pop(0) if not peep else self.line_buffer[0]
            else:
                return -1


class StringSourceProcessor(BaseSourceProcessor):
    """character peeker for files."""

    def __init__(self, string_source: str):
        super(StringSourceProcessor, self).__init__()
        self.cursor: Cursor = Cursor(0, 0)
        self.buffer: List[str] = list(self.pretreatment(string_source))

    def pretreatment(self, string: str) -> str:
        """reduce redundant whitespace and return the str"""
        string: str = string.replace('\t', '').replace('\r', '')
        return ' '.join([ch for ch in string.split(' ') if ch != ''])

    def next_char(self, peep=False):
        if self.buffer:
            self.cursor.col += 1 if not peep else 0
            self.cursor.line += 1 if not peep and self.buffer[0] == '\n' else 0
            return self.buffer.pop(0) if not peep else self.buffer[0]
        else:
            return -1
