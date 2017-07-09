"""test case for lexer"""
import pytest
from src.lexer import Lexer
from src.source import FileSource, StringSource

class TestLexer:
    """
    test lexer
    """

    @pytest.fixture(autouse=True)
    def test_init(self, test_source_file):
        with open(test_source_file, 'r') as file_obj:
            print(file_obj.read)

    def test_file_lexical_analysis(self, test_source_file):
        source = FileSource(test_source_file)
        lexer = Lexer(source)
        lexer.match()
        print(lexer.token_list)

    def test_string_lexical_analysis(self, test_source_string):
        source = StringSource(test_source_string)
        lexer = Lexer(source)
        lexer.match()
        print(lexer.token_list)
