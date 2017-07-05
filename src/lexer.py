"""
Lexer generate tokens for parsing.
"""
from src.token import Token, Position
from src.exceptions import InvalidTokenException
from typing import List


token_type = ("KW", "ID", "OP", "DIM", "VAL", "EOF", "INVALID")
keywords = ("if", "else", "then", "case", "while", "do", "break", "continue", "return", "switch", "default")
var_types = ("int", "float", "char", "bool")
delimiters = (",", ";", ":", "(", ")", "[", "]", "{", "}")
operators = ("+", "++", "-", "--", "*", "**", "/", "//", "<", "<=", "=", "==", "!=", ">", ">=", "&", "|", "!")


class Lexer(object):

    def __init__(self):
        self.pointer: Position = Position(0, 0)
        self.read_buffer: List[str] = []
        self.token_list: List[Token] = []
        self.char_peeker = None

    def create_token(self, t_type: str, token) -> Token:
        self.token_list.append(Token(t_type, token))

    def match_identifier(self) -> str:
        while True:
            next_char = self.char_peeker.next_char()
            if next_char is self.char_peeker.lineEnd or not next_char.isalpha() and not next_char.isdigit() and next_char != '_':
                return ''.join(self.read_buffer)
            self.read_buffer.append(next_char)

    def match_digit(self) -> int:
        while True:
            next_char = self.char_peeker.next_char()
            if next_char == '.':
                self.read_buffer.append(next_char)
                return self.match_float()
            elif next_char is self.char_peeker.lineEnd or not next_char.isdigit():
                return eval(''.join(self.read_buffer))
            self.read_buffer.append(next_char)

    def match_float(self) -> float:
        while True:
            next_char = self.char_peeker.next_char()
            if next_char is self.char_peeker.lineEnd or not next_char.isdigit():
                return eval(''.join(self.read_buffer))
            self.read_buffer.append(next_char)

    def match_line_comment(self) -> str:
        while True:
            next_char = self.char_peeker.next_char()
            if next_char is self.char_peeker.lineEnd:
                return ''.join(self.read_buffer)
            self.read_buffer.append(next_char)

    def match_block_comment(self) -> str:
        pass

    def match_operator(self, operators) -> str:
        while True:
            next_char = self.char_peeker.next_char()
            if next_char is self.char_peeker.lineEnd or next_char not in operators:
                return ''.join(self.read_buffer)
            self.read_buffer.append(next_char)
        next_char = self.char_peeker.next_char()

    def match(self):
        
