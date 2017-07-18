"""test module for transform concrete syntax tree to abstract syntax tree."""
import pytest
from src.token import TokenSource
from src.lexer import Lexer
from src.parser import ParseTranslationUnit
from src.ast import SourceRoot
from src.source import FileSource

class TestParser:
    """
    test transform.
    """

    @pytest.fixture(autouse=True)
    def test_init(self, test_source_file):
        with open(test_source_file, 'r') as file_obj:
            print(file_obj.read)
        source = FileSource(test_source_file)
        lexer = Lexer(source)
        lexer.match()
        print(lexer.token_list)
        token_source = TokenSource(lexer.token_list)
        self.cst = ParseTranslationUnit.parse(token_source)

    def test_transform(self):
        ast = SourceRoot.transform(self.cst)
        print(ast)
