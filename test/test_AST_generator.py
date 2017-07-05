# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-04-15 12:28:18
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-04-15 13:35:33
import pytest
from src.util import SyntexTreeGenerator
from src import exceptions


class TestASTGenerator:
    """test class for AST generation.

    test both fine regular expression AST generate and bad regular
    expression exceptions raises.
    """

    @pytest.fixture(autouse=True)
    def test_init(self, expression):
        print(expression['fineExpressions'])
        print(expression['badExpressions'])

    def test_generate_tree(self, expression):
        for expression in expression['fineExpressions']:
            tree = SyntexTreeGenerator.NonTerminalSymbol_E().parse(expression)
            print(tree)

    def test_exception_handle(self, expression):
        for expression in expression['badExpressions']:
            with pytest.raises(exceptions.ParseError):
                SyntexTreeGenerator.NonTerminalSymbol_E().parse(expression)
