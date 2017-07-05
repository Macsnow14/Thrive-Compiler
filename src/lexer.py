"""
Lexer generate tokens for parsing.
"""
from src.token import Token, Position
from src.exceptions import InvalidTokenException
from typing import List


class Lexer(object):

    def __init__(self):
        self.pointer: Position = Position(0, 0)
        self.read_buffer: List[str] = []
        self.token_list: List[Token] = []
        self.char_peeker = None

    def createToken(self, t_type: str, token) -> Token:
        self.token_list.append(Token(t_type, token))

    def matchIdentifier(self) -> str:
        while True:
            next_char = self.char_peeker.next_char()
            if next_char is self.char_peeker.lineEnd or not next_char.isalpha() and not next_char.isdigit() and next_char != '_':
                return ''.join(self.read_buffer)
            self.read_buffer.append(next_char)

    def matchDigit(self) -> int:
        while True:
            next_char = self.char_peeker.next_char()
            if next_char == '.':
                self.read_buffer.append(next_char)
                return self.matchFloat()
            elif next_char is self.char_peeker.lineEnd or not next_char.isdigit():
                return eval(''.join(self.read_buffer))
            self.read_buffer.append(next_char)

    def matchFloat(self) -> float:
        while True:
            next_char = self.char_peeker.next_char()
            if next_char is self.char_peeker.lineEnd or not next_char.isdigit():
                return eval(''.join(self.read_buffer))
            self.read_buffer.append(next_char)

    def matchLineComment(self) -> str:
        while True:
            next_char = self.char_peeker.next_char()
            if next_char is self.char_peeker.lineEnd:
                return ''.join(self.read_buffer)
            self.read_buffer.append(next_char)

    def matchBlockComment(self) -> str:
        pass

    def matchOperator(self, operators) -> str:
        next_char = self.char_peeker.next_char()
        if next_char in operators:
            
        

    def match(self):
        pass
