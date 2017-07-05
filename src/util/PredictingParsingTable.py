"""
module for generate predicting parsing table.
"""
from collections import defaultdict
from typing import List, Dict, Set, Tuple
import copy
import json


class ParsingTableGenerator(object):
    """
    class for generate predicting parsing table.
    """

    def __init__(self, grammar: str, terminators: tuple, non_terminators: tuple):
        self.p_list: List[Tuple[str, List[str]]
                         ] = self.convert_grammar(grammar)
        self.terminators: Tuple[str] = terminators
        self.non_terminators: Tuple[str] = non_terminators
        self.first_dict: Dict[str, Set[str]] = self.first_constructor()
        self.follow_dict: Dict[str, Set[str]] = self.follow_constructor()
        self.parsing_table: Dict[Tuple[str], Tuple[str, List[str]]] = None

    def convert_grammar(self, grammar: str) -> List[Tuple[str, List[str]]]:
        """convert grammar from string to tuple"""
        self.p_list: List[Tuple[str, List[str]]] = list()
        for production_rule in grammar:
            production_rule: str = production_rule.replace(' ', '')
            m_list: List[str] = production_rule.split('->')
            self.p_list.append((m_list[0], list(m_list[1])))
        return self.p_list

    def first_constructor(self) -> Dict[str, Set[str]]:
        """construct first set."""
        first_dict: Dict[str, Set[str]] = defaultdict(set)
        for production_rule in self.p_list:
            non_terminator: str = production_rule[0]
            first_dict[non_terminator]: Set[str] = self.find_first(
                non_terminator)
        return first_dict

    def find_first(self, symbol) -> Set[str]:
        """to find a non-terminator's first set."""
        first_set: Set[str] = set()
        if symbol not in self.non_terminators:
            first_set.add(symbol)
        else:
            first_set |= set([production_rule[1][0] for production_rule in self.p_list if production_rule[0]
                              == symbol and production_rule[1][0] not in self.non_terminators])
            for production_rule in self.p_list:
                if production_rule[0] == symbol and production_rule[1][0] in self.non_terminators:
                    first_set |= self.find_first(
                        production_rule[1][0]) - set(('ε'))
            first_set -= set([None])
        return first_set

    def find_first_string(self, symbols) -> Set[str]:
        """to find a string of symbols first set."""
        first_set: Set[str] = set()
        for symbol in symbols:
            first_set |= self.find_first(symbol) - set(('ε'))
            if 'ε' not in self.find_first(symbol):
                break
            elif symbol is symbols[-1]:
                first_set.add('ε')
        return first_set

    def follow_constructor(self) -> Dict[str, Set[str]]:
        """consturct follow set"""
        follow_dict: Dict[str, Set[str]] = defaultdict(set)
        for production_rule in self.p_list:
            if production_rule[0] is 'E':
                follow_dict[production_rule[0]].add('#')
            for i, symbol in enumerate(production_rule[1]):
                if symbol in self.non_terminators and symbol is not production_rule[1][-1]:
                    follow_dict[symbol] |= self.find_first(
                        production_rule[1][i + 1]) - set(('ε'))

        for production_rule in self.p_list:
            for i, symbol in enumerate(production_rule[1]):
                if symbol in self.non_terminators:
                    if symbol is production_rule[1][-1]:
                        follow_dict[symbol] |= follow_dict[production_rule[0]]
                    else:
                        if 'ε' in self.find_first_string(production_rule[1][i + 1:]):
                            follow_dict[symbol] |= follow_dict[production_rule[0]]
        return follow_dict

    def table_constractor(self) -> Dict[Tuple[str], Tuple[str, List[str]]]:
        """construct predicting parsing table."""
        self.parsing_table: Dict[Tuple[str],
                                 Tuple[str, List[str]]] = defaultdict(tuple)
        for production_rule in self.p_list:
            if 'ε' in self.find_first_string(production_rule[1]):
                for symbol in self.follow_dict[production_rule[0]]:
                    self.parsing_table[(production_rule[0], symbol)
                                       ]: Tuple[str, List[str]] = production_rule
                if '#' in self.follow_dict[production_rule[0]]:
                    self.parsing_table[(production_rule[0], '#')
                                       ]: Tuple[str, List[str]] = production_rule
            for symbol in self.terminators:
                if symbol in self.find_first_string(production_rule[1]):
                    self.parsing_table[(production_rule[0], symbol)
                                       ]: Tuple[str, List[str]] = production_rule
        return self.parsing_table


def parseDict(AST):
    """
    parse AST to dict obj.
    """
    return {'symbol': AST.symbol,
            'child': [parseDict(node) for node in AST.child if AST.child]}


def predictingParsing(parsing_table, stack, string, non_terminators):
    stack.append('#')
    stack.append('E')
    IP = 0
    p_seq = []
    while True:
        # AST.child = parsing_table[stack[-1], string[IP]][1]
        if len(stack) == 0:
            break
        elif stack[-1] in non_terminators:
            production_rule = parsing_table[stack[-1], string[IP]]
            p_seq.append(production_rule)
            stack.pop()
            if 'ε' not in production_rule[1]:
                reversed_p = copy.copy(production_rule[1])
                reversed_p.reverse()
                stack += reversed_p
        elif stack[-1] == string[IP]:
            stack.pop()
            IP += 1
        else:
            raise Exception('asdasd')

    return p_seq


def ASTGenerator(ast_root, p_seq, non_terminators):
    if len(p_seq) != 0:
        ast_root.child = [AST(node) for node in p_seq.pop(0)[1]]
        for ast_node in ast_root.child:
            if ast_node.symbol in non_terminators:
                ASTGenerator(ast_node, p_seq, non_terminators)
    else:
        return


class AST(object):
    """
    Abstract Sytex Tree
    """

    def __init__(self, symbol):
        self.symbol = symbol
        self.child = list()

    def __str__(self):
        return json.dumps(parseDict(self), indent=2)


if __name__ == '__main__':
    grammar = ('E -> TR',
               'R -> +TR',
               'R -> -TR',
               'R -> ε',
               'T -> (E)',
               'T -> i',
               'T -> n')

    non_terminators = ('E', 'T', 'R')
    terminators = ('i', 'n', '(', ')', '+', '-')

    parsingTableGenerator = ParsingTableGenerator(
        grammar, terminators, non_terminators)

    parsing_table = parsingTableGenerator.table_constractor()
    print(parsingTableGenerator.p_list)
    print(parsingTableGenerator.first_dict)
    print(parsingTableGenerator.follow_dict)
    print(parsing_table)

    string = "i+i-(i+i)#"
    string = list(string)
    stack = []

    syntaxTree = dict()

    p_seq = predictingParsing(parsing_table, stack, string, non_terminators)
    print(p_seq)

    ast_root = AST(p_seq[0][0])
    ASTGenerator(ast_root, p_seq, non_terminators)

    print(ast_root)
