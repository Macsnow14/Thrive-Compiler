import pytest
from src.util import PredictingParsingTable
from src import exceptions


class TestASTGenerator:
    """test class for AST generation.

    test both fine regular expression AST generate and bad regular
    expression exceptions raises.
    """

    @pytest.fixture(autouse=True)
    def test_init(self, test_grammar):
        print(test_grammar['grammar'])
        print(test_grammar['terminators'])
        print(test_grammar['non_terminators'])

    def test_generate_table(self, test_grammar):
        generator = PredictingParsingTable.ParsingTableGenerator(test_grammar['grammar'],
                                                                 test_grammar['terminators'],
                                                                 test_grammar['non_terminators'])
        print(generator.table_constractor())
