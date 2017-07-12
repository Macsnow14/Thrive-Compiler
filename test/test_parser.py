"""test module for parser"""
import pytest
from src.token import TokenSource
from src.lexer import Lexer
from src.parser import ParsetranslationUnit
from src.source import FileSource

class TestParser:
    """
    test parser
    """

    @pytest.fixture(autouse=True)
    def test_init(self, test_source_file):
        with open(test_source_file, 'r') as file_obj:
            print(file_obj.read)
        source = FileSource(test_source_file)
        lexer = Lexer(source)
        lexer.match()
        print(lexer.token_list)
        self.token_source = TokenSource(lexer.token_list)

    def test_parsing(self, test_source_file):
        ast = ParsetranslationUnit.parse(self.token_source)
        print(ast)
