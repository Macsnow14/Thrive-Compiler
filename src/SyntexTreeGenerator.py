# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-04-12 20:40:35
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-04-15 13:28:59
from .Exceptions import ParseError
import json
"""this module is enlightened by zccz14's Visual-Compiler:
[regexp.ts](https://github.com/zccz14/Visual-Compiler/blob/master/src/lib/regexp.ts)

To generate a AST from a given regular expression.
"""


NonCharSymbol = ('|', '*', '(', ')')


def isCharactor(symbol):
    """
    to judge if a symbol is a charactor.
    """
    if symbol in NonCharSymbol:
        return False
    else:
        return True


def parseDict(AST):
    """
    parse AST to dict obj.
    """
    return {'symbol': AST.symbol,
            'child': [parseDict(node) for node in AST.child if AST.child]}


class Expression(object):
    """
    An expression who can walk.
    """

    def __init__(self, expression):
        self.expression = expression
        self.ip = 0

    def __repr__(self):
        return self.expression

    def get(self):
        self.ip += 1
        return self.expression[self.ip - 1]

    def judge(self):
        try:
            return '<Charactor>' if isCharactor(self.expression[self.ip]) else self.expression[self.ip]
        except IndexError:
            return '<Epsilon>'

    def accept(self):
        self.ip += 1


class AST(object):
    """
    Abstract Syntex Tree base class
    """
    firstSet = set()

    def __init__(self, symbol):
        self.symbol = symbol
        self.child = list()
        self.process = dict()

    def parse(expression):
        raise NotImplementedError

    def __str__(self):
        return json.dumps(parseDict(self), indent=2)


class NonTerminalSymbol_E(AST):
    """
    E -> (E)T|<Charactor>T

    NonTerminal symbol for E
    """
    firstSet = set(('(', '<Charactor>'))

    def __init__(self):
        super(NonTerminalSymbol_E, self).__init__('E')

    def parse(self, expression):
        if expression.judge() == '(':
            self.child.append(TerminalSymbol(expression.get()))
            self.child.append(NonTerminalSymbol_E().parse(expression))
            if expression.judge() == ')':
                self.child.append(TerminalSymbol(expression.get()))
            else:
                raise ParseError('parse error: unexpect symbol \'%s\' in %d' % (expression.judge(), expression.ip))

            self.child.append(NonTerminalSymbol_T().parse(expression))

        elif expression.judge() == '<Charactor>':
            self.child.append(TerminalSymbol(expression.get()))

            self.child.append(NonTerminalSymbol_T().parse(expression))

        else:
            raise ParseError('parse error: unexpect symbol \'%s\' in %d' % (expression.judge(), expression.ip))

        return self


class NonTerminalSymbol_F(AST):
    """
    F -> E|or E|*

    NonTerminal symbol for F
    """
    firstSet = set(('|', '*')) | NonTerminalSymbol_E.firstSet

    def __init__(self):
        super(NonTerminalSymbol_F, self).__init__('F')

    def parse(self, expression):
        if expression.judge() in NonTerminalSymbol_E.firstSet:
            self.child.append(NonTerminalSymbol_E().parse(expression))

        elif expression.judge() == '|':
            self.child.append(TerminalSymbol(expression.get()))
            self.child.append(NonTerminalSymbol_E().parse(expression))

        elif expression.judge() == '*':
            self.child.append(TerminalSymbol(expression.get()))

        else:
            raise ParseError('parse error: unexpect symbol \'%s\' in %d' % (expression.judge(), expression.ip))

        return self


class NonTerminalSymbol_T(AST):
    """
    T -> FT|<Epsilon>

    NonTerminal symbol for T
    """
    firstSet = set(('<Epsilon>')) | NonTerminalSymbol_F.firstSet

    def __init__(self):
        super(NonTerminalSymbol_T, self).__init__('T')

    def parse(self, expression):
        if expression.judge() in NonTerminalSymbol_F.firstSet:
            self.child.append(NonTerminalSymbol_F().parse(expression))
            self.child.append(NonTerminalSymbol_T().parse(expression))

        return self


class TerminalSymbol(AST):
    """
    TerminalSymbols
    """

    def __init__(self, symbol):
        super(TerminalSymbol, self).__init__(symbol)

    def parse(self):
        return self


if __name__ == '__main__':
    expression = Expression('1(0|1)*101')
    tree = NonTerminalSymbol_E().parse(expression)
    print(tree)
