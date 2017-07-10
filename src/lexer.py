"""
Lexer generate tokens for parsing.
"""
from typing import List
from src.token import Token
from src.source import BaseSource
from src.exceptions import InvalidTokenException


token_type = ("KW", "ID", "OP", "DIM", "VAL", "EOF", "INVALID")
keywords = ("if", "else", "then", "case", "while", "do", "break", "continue", "return", "switch", "default", "int", "float", "char", "bool")
var_types = ("int", "float", "char", "bool")
delimiters = (",", ";", ":", "(", ")", "[", "]", "{", "}")
operators = ("+", "-", "*", "/", "<", "=", ">", "&", "|", "!")


class Lexer(object):
    """Lexical analyzer to generate token from source code."""

    def __init__(self, file_source: BaseSource):
        self.read_buffer: List[str] = []
        self.token_list: List[Token] = []
        self.src: BaseSource = file_source

    def create_token(self, t_type: str, token_literal: str) -> Token:
        """create token from string"""
        token: Token = Token(t_type, token_literal, self.src)
        self.token_list.append(token)
        return token

    def match_literal(self) -> str:
        """match literal elements(identifier, keyword, true and false value)"""
        while True:
            next_char: str = self.src.next_char(True)
            if next_char == ' ' or self.src.is_line_end(next_char) or next_char in delimiters or next_char in operators:
                token_literal: str = ''.join(self.read_buffer)
                if token_literal == 'true':
                    return self.create_token('VAL', True)
                elif token_literal == 'flase':
                    return self.create_token('VAL', False)
                else:
                    return self.create_token('KW' if token_literal in keywords else 'ID', token_literal)
            elif not next_char.isalpha() and not next_char.isdigit() and next_char != '_':
                raise InvalidTokenException("illegal character %s appeared" % next_char)
            elif next_char == -1:
                raise InvalidTokenException("unexpected EOF")
            self.read_buffer.append(self.src.next_char())

    def match_character(self) -> str:
        """match character elements"""
        self.src.next_char()
        next_char: str = self.src.next_char()
        self.read_buffer.append(next_char)
        if next_char == '\\':
            next_char: str = self.src.next_char()
            self.read_buffer.append(next_char)
        if next_char == '\'':
            token_literal: str = ''.join(self.read_buffer)
            return self.create_token('VAL', token_literal)
        else:
            raise InvalidTokenException("character must be quote in apostrophes.")

    def match_string(self) -> str:
        """match char array elements"""
        self.src.next_char()
        while True:
            next_char: str = self.src.next_char()
            if next_char =='\"':
                token_literal: str = ''.join(self.read_buffer)
                return self.create_token('VAL', token_literal)
            elif self.src.is_line_end(next_char):
                raise InvalidTokenException("unclosed quote")
            elif next_char == -1:
                raise InvalidTokenException("unexpected EOF")

    def match_digit(self) -> int:
        """match digit element"""
        while True:
            next_char: str = self.src.next_char(True)
            if next_char == '.':
                self.read_buffer.append(next_char)
                return self.match_float()
            elif next_char == ' ' or self.src.is_line_end(next_char) or next_char in delimiters:
                token_literal: str = ''.join(self.read_buffer)
                return self.create_token('VAL', token_literal)
            elif not next_char.isdigit():
                raise InvalidTokenException("illegal character %s appeared" % next_char)
            elif next_char == -1:
                raise InvalidTokenException("unexpected EOF")
            self.read_buffer.append(self.src.next_char())

    def match_float(self) -> float:
        """match float element"""
        while True:
            next_char = self.src.next_char(True)
            if next_char == ' ' or self.src.is_line_end(next_char) or next_char in delimiters:
                token_literal: str = ''.join(self.read_buffer)
                return self.create_token('VAL', token_literal)
            elif not next_char.isdigit():
                raise InvalidTokenException("illegal character %s appeared" % next_char)
            elif next_char == -1:
                raise InvalidTokenException("unexpected EOF")
            self.read_buffer.append(self.src.next_char())

    def match_line_comment(self) -> None:
        """match line comment element"""
        while True:
            next_char = self.src.next_char()
            if self.src.is_line_end(next_char) or next_char == -1:
                return
            self.read_buffer.append(next_char)

    def match_operator(self) -> str:
        """match operator element"""
        next_char = self.src.next_char()
        self.read_buffer.append(next_char)
        if next_char == '+':
            self._peek_next_tk('+')
        elif next_char == '-':
            self._peek_next_tk('-')
        elif next_char == '=':
            self._peek_next_tk('=')
        elif next_char == '!':
            self._peek_next_tk('=')
        elif next_char == '>':
            self._peek_next_tk('=')
        elif next_char == '<':
            self._peek_next_tk('=')
        elif next_char == '&':
            self._peek_next_tk('&')
        elif next_char == '|':
            self._peek_next_tk('|')
        token_literal: str = ''.join(self.read_buffer)
        return self.create_token('OP', token_literal)

    def _peek_next_tk(self, token, harsh=False):
        """to see if a token is binocular operator."""
        if self.src.next_char(True) == token:
            next_char = self.src.next_char()
            self.read_buffer.append(next_char)
        elif harsh:
            raise InvalidTokenException("token %s invalid" % (token))

    def match_delimiters(self):
        """match delimiter elements"""
        next_char = self.src.next_char()
        self.read_buffer.append(next_char)
        token_literal: str = ''.join(self.read_buffer)
        return self.create_token('DIM', token_literal)

    def match(self):
        """match engine"""
        while True:
            peek_next_char: str = self.src.next_char(True)
            if peek_next_char == -1:
                break
            if peek_next_char.isalpha():
                self.match_literal()
            elif peek_next_char.isdigit():
                self.match_digit()
            elif peek_next_char == '#':
                self.match_line_comment()
            elif peek_next_char in operators:
                self.match_operator()
            elif peek_next_char in delimiters:
                self.match_delimiters()
            elif self.src.is_line_end(peek_next_char) or peek_next_char == ' ':
                self.src.next_char()
            else:
                raise InvalidTokenException
            self.read_buffer = []
