"""
paser to generate quaternary.

Recursive descent parsing.
"""
import json
from typing import List
from .token import Token, TokenSource
from .lexer import var_types
from .exceptions import ParseException

# TODO: add judgement static method to each class.


def parse_dict(parse_node):
    """
    parse AST to dict obj.
    """
    return {'symbol': parse_node.token if isinstance(parse_node.token, str) else parse_node.token.value,
            'child': [parse_dict(node) for node in parse_node.child if parse_node.child]}


class ParseNode(object):
    """
    Abstract Syntex Tree base class
    """

    def __init__(self, token: Token or str):
        self.token: Token = token
        self.child: List[ParseNode] = list()

    def __str__(self):
        return json.dumps(ParseNode.parse_dict(self), indent=2)

    @staticmethod
    def parse_dict(parse_node):
        """
        parse AST to dict obj.
        """
        return {'symbol': parse_node.token if isinstance(parse_node.token, str) else parse_node.token.value,
                'child': [ParseNode.parse_dict(node) for node in parse_node.child if parse_node.child]}


class ParseToken(ParseNode):
    """
    Token as the terminator.
    """

    @classmethod
    def parse(cls, token_source: TokenSource):
        """parse token source to recursively construct a node."""
        return cls(token_source.get())


class ParseTranslationUnit(ParseNode):
    """
    BNF:
    translation_unit    : external_decl
                        | translation_unit external_decl
                        ;

    EBNF:
    translation_unit    : external_decl { external_decl }
                        ;

    parse translation unit.
    the origin symbol.
    """

    @classmethod
    def parse(cls, token_source: TokenSource):
        """parse token source to recursively construct a node."""
        node = cls('translation Unit')

        node.child.append(ParseExternalDecl.parse(token_source))
        while token_source.peek(1).value in var_types:
            node.child.append(ParseExternalDecl.parse(token_source))

        return node


class ParseExternalDecl(ParseNode):
    """
    BNF:
    external_decl       : type_spec function_definition
                        | type_spec init_declarator_list ';'
                        ;
    EBNF:
    external_decl       : type_spec ( function_definition | init_declarator_list ';')
                        ;

    parse external declaration.
    """
    @classmethod
    def parse(cls, token_source: TokenSource):
        """parse token source to recursively construct a node."""
        node = cls('external declaration')

        node.child.append(ParseTypeSpec.parse(token_source))
        if token_source.peek(1).type == 'ID':
            if token_source.peek(2).value == '(':
                node.child.append(
                    ParseFunctionDefinition.parse(token_source))
            else:
                node.child.append(
                    ParseInitDeclaratorList.parse(token_source))
                node.child.append(ParseToken.parse(token_source))

        return node


class ParseFunctionDefinition(ParseNode):
    """
    BNF:
    function_definition : declarator compound_stat
                        ;
    EBNF:
    function_definition : declarator compound_stat
                        ;

    parse function definition.
    """

    @classmethod
    def parse(cls, token_source: TokenSource):
        """parse token source to recursively construct a node."""
        node = cls("function definition")

        node.child.append(ParseDeclarator.parse(token_source))
        node.child.append(ParseCompoundStat.parse(token_source))

        return node


class ParseDecl(ParseNode):
    """
    BNF:
    decl		        : type_spec init_declarator_list ';'
                        ;
    EBNF:
    decl		        : type_spec init_declarator_list ';'
                        ;

    parse declaration.
    """

    @classmethod
    def parse(cls, token_source: TokenSource):
        """parse token source to recursively construct a node."""
        node = cls('declaration')

        node.child.append(ParseTypeSpec.parse(token_source))
        node.child.append(ParseInitDeclaratorList.parse(token_source))
        if token_source.peek(1).value == ';':
            node.child.append(ParseToken.parse(token_source))
        else:
            raise ParseException("at %s, declaration must end up with ';'." % (
                token_source.peek(1).cursor))

        return node


class ParseDeclList(ParseNode):
    """
    BNF:
    decl_list               : decl
                            | decl_list decl
                            ;
    EBNF:
    decl_list               : decl { decl }
                            ;

    parse declaration list.
    """

    @classmethod
    def parse(cls, token_source: TokenSource):
        """parse token source to recursively construct a node."""
        node = cls("declaration list")

        node.child.append(ParseDecl.parse(token_source))
        while token_source.peek(1).value in var_types:
            node.child.append(ParseDecl.parse(token_source))

        return node


class ParseTypeSpec(ParseNode):
    """
    BNF:
    type_spec               : 'char' | 'int' | 'bool' | 'float'
                            ;
    EBNF:
    type_spec               : 'char' | 'int' | 'bool' | 'float'
                            ;

    parse type spec.
    """
    @staticmethod
    def is_type_spec(token_source):
        return token_source.peek(1).value in var_types

    @classmethod
    def parse(cls, token_source: TokenSource):
        """parse token source to recursively construct a node."""
        if cls.is_type_spec(token_source):
            return cls(token_source.get())
        else:
            raise ParseException('at %s, %s is not a var type, expect var type' % (
                token_source.peek(1).cursor,
                token_source.peek(1).value))


class ParseInitDeclaratorList(ParseNode):
    """
    BNF:
    init_declarator_list    : init_declarator
                            | init_declarator_list ',' init_declarator
                            ;
    EBNF:
    init_declarator_list    : init_declarator { ',' init_declarator }
                            ;

    parse init declarator list.
    """

    @classmethod
    def parse(cls, token_source: TokenSource):
        """parse token source to recursively construct a node."""
        node = cls("init declarator list")

        node.child.append(ParseInitDeclarator.parse(token_source))
        while token_source.peek(1).value == ',':
            node.child.append(ParseNode(token_source.get()))
            node.child.append(ParseInitDeclarator.parse(token_source))

        return node


class ParseInitDeclarator(ParseNode):
    """
    BNF:
    init_declarator         : declarator
                            | declarator '=' initializer
                            ;
    EBNF:
    init_declarator         : declarator [ '=' initializer ]
                            ;

    parse init declarator.
    """

    @classmethod
    def parse(cls, token_source: TokenSource):
        """parse token source to recursively construct a node."""
        node = cls("init declarator")

        node.child.append(ParseDeclarator.parse(token_source))
        if token_source.peek(1).value == '=':
            node.child.append(ParseToken.parse(token_source))
            node.child.append(ParseInitializer.parse(token_source))

        return node


class ParseDeclarator(ParseNode):
    """
    BNF:
    declarator              : id
                            | declarator '[' logical_or_exp ']'
                            | declarator '['		']'
                            | declarator '(' param_list ')'
                            | declarator '(' id_list ')'
                            | declarator '('		')'
                            ;
    EBNF:
    declarator              : id { '[' [ logical_or_exp ] ']' |
                                   '(' [ param_list ] ')' |
                                   '(' [ id_list ] ')' }
                            ;

    parse declarator.
    """

    # TODO: cat function declaration down.
    @classmethod
    def parse(cls, token_source: TokenSource):
        """parse token source to recursively construct a node."""
        node = cls("declarator")

        if token_source.peek(1).type == 'ID':
            node.child.append(ParseToken.parse(token_source))
            while token_source.peek(1).value in ('[', '('):
                if token_source.peek(1).value == '[':
                    node.child.append(ParseToken.parse(token_source))
                    if token_source.peek(1).type in ('ID', 'VAL') or token_source.peek(1).value in ('(', '+', '-', '!', '++', '--'):
                        node.child.append(
                            ParseLogicalOrExp.parse(token_source))
                    if token_source.peek(1).value == ']':
                        node.child.append(ParseToken.parse(token_source))
                    else:
                        raise ParseException("at %s, expect ']'" % (
                            token_source.peek(1).cursor))
                elif token_source.peek(1).value == '(':
                    node.child.append(ParseToken.parse(token_source))
                    if token_source.peek(1).value in var_types:
                        node.child.append(ParseParamList.parse(token_source))
                    elif token_source.peek(1).type == 'ID':
                        node.child.append(ParseIdList.parse(token_source))
                    if token_source.peek(1).value == ')':
                        node.child.append(ParseToken.parse(token_source))
                    else:
                        raise ParseException("'%s' is not ')', expect ')'" % (
                            token_source.peek(1).value))
        else:
            raise ParseException("at %s, '%s' is not ID, expect ID." % (token_source.peek(1).cursor,
                                                                        token_source.peek(1).value))

        return node


class ParseParamList(ParseNode):
    """
    BNF:
    param_list              : param_decl
                            | param_list ',' param_decl
                            ;
    EBNF:
    param_list              : param_decl { ',' param_decl }
                            ;

    parse param list.
    """

    @classmethod
    def parse(cls, token_source: TokenSource):
        """parse token source to recursively construct a node."""
        node = cls("param list")

        node.child.append(ParseParamDecl.parse(token_source))
        while token_source.peek(1).value == ',':
            node.child.append(ParseToken.parse(token_source))
            node.child.append(ParseParamDecl.parse(token_source))

        return node


class ParseParamDecl(ParseNode):
    """
    BNF:
    param_decl              : type_spec declarator
                            | type_spec
                            ;
    EBNF:
    param_decl              : type_spec { declarator }
                            ;

    parse param decl.
    """

    # FIXME: EBNF is a wrong one.
    @classmethod
    def parse(cls, token_source: TokenSource):
        """parse token source to recursively construct a node."""
        node = cls("param decl")

        node.child.append(ParseToken.parse(token_source))
        while token_source.peek(1).type == 'ID':
            node.child.append(ParseDeclarator.parse(token_source))

        return node


class ParseIdList(ParseNode):
    """
    BNF:
    id_list                 : id
                            | id_list ',' id
                            ;
    EBNF:
    id_list                 : id { ',' id }
                            ;

    parse Id list.
    """

    @classmethod
    def parse(cls, token_source: TokenSource):
        """parse token source to recursively construct a node."""
        node = cls("Id list")

        if token_source.peek(1).type == 'ID':
            node.child.append(ParseToken.parse(token_source))
            while token_source.peek(1).value == ',':
                node.child.append(ParseToken.parse(token_source))
                if token_source.peek(1).type == 'ID':
                    node.child.append(ParseToken.parse(token_source))
                else:
                    raise ParseException("at %s, expect ID" %
                                         (token_source.peek(1).cursor))
        else:
            raise ParseException("at %s, expect ID" %
                                 (token_source.peek(1).cursor))

        return node


class ParseInitializer(ParseNode):
    """
    BNF:
    initializer             : assignment_exp
                            | '{' initializer_list '}'
                            | '{' initializer_list ',' '}'
                            ;
    EBNF:
    initializer             : assignment_exp
                            | '{' initializer_list [ ',' ] '}'
                            ;
    parse initializer.
    """

    @classmethod
    def parse(cls, token_source: TokenSource):
        """parse token source to recursively construct a node."""
        node = cls("initializer")

        if token_source.peek(1).value == '{':
            node.child.append(ParseToken.parse(token_source))
            node.child.append(ParseInitDeclaratorList.parse(token_source))
            if token_source.peek(1).value == ',':
                node.child.append(ParseToken.parse(token_source))
            if token_source.peek(1).value == '}':
                node.child.append(ParseToken.parse(token_source))
        else:
            node.child.append(ParseAssignmentExp.parse(token_source))

        return node


class ParseInitializerList(ParseNode):
    """
    BNF:
    initializer_list        : initializer
                            | initializer_list ',' initializer
                            ;
    EBNF:
    initializer_list        : initializer { ',' initializer }
                            ;
    parse initializer list.
    """

    @classmethod
    def parse(cls, token_source: TokenSource):
        """parse token source to recursively construct a node."""
        node = cls("initializer list")

        node.child.append(ParseInitializer.parse(token_source))
        while token_source.peek(1).value == ',':
            node.child.append(ParseToken.parse(token_source))
            node.child.append(ParseInitializer.parse(token_source))

        return node


class ParseStatement(ParseNode):
    """
    BNF:
    stat                    : labeled_stat
                            | exp_stat
                            | compound_stat
                            | selection_stat
                            | iteration_stat
                            | jump_stat
                            ;
    EBNF:
    stat                    : labeled_stat
                            | exp_stat
                            | compound_stat
                            | selection_stat
                            | iteration_stat
                            | jump_stat
                            ;
    parse statement.
    """
    @staticmethod
    def is_stat(token_source):
        return ParseStatement.is_labeled_stat(token_source) or ParseStatement.is_exp_stat(token_source) or ParseStatement.is_compound_stat(token_source) or ParseStatement.is_selection_stat(token_source) or ParseStatement.is_iteration_stat(token_source) or ParseStatement.is_jump_stat(token_source)

    @staticmethod
    def is_labeled_stat(token_source):
        return token_source.peek(2).value == ':' or token_source.peek(1).value == 'case' or token_source.peek(1).value == 'default'

    @staticmethod
    def is_exp_stat(token_source):
        return token_source.peek(1).type in ('ID', 'VAL') or token_source.peek(1).value in ('(', '+', '-', '!', '++', '--', ';')

    @staticmethod
    def is_compound_stat(token_source):
        return token_source.peek(1).value == '{'

    @staticmethod
    def is_selection_stat(token_source):
        return token_source.peek(1).value in ('if', 'switch')

    @staticmethod
    def is_iteration_stat(token_source):
        return token_source.peek(1).value in ('while', 'do')

    @staticmethod
    def is_jump_stat(token_source):
        return token_source.peek(1).value in ('continue', 'break', 'return')

    @classmethod
    def parse(cls, token_source: TokenSource):
        """parse token source to recursively construct a node."""
        node = cls("statement")

        if cls.is_labeled_stat(token_source):
            node.child.append(ParseLabeledStat.parse(token_source))
        elif cls.is_exp_stat(token_source):
            node.child.append(ParseExpStat.parse(token_source))
        elif cls.is_compound_stat(token_source):
            node.child.append(ParseCompoundStat.parse(token_source))
        elif cls.is_selection_stat(token_source):
            node.child.append(ParseSelectionStat.parse(token_source))
        elif cls.is_iteration_stat(token_source):
            node.child.append(ParseIterationStat.parse(token_source))
        elif cls.is_jump_stat(token_source):
            node.child.append(ParseJumpStat.parse(token_source))
        else:
            raise ParseException("at %s, expect Statement" %
                                 (token_source.peek(1).cursor))
        # NOTE: maybe using a loop would avoid these ugly selection statements?
        return node


class ParseLabeledStat(ParseNode):
    """
    BNF:
    labeled_stat            : id ':' stat
                            | 'case' logical_or_exp ':' stat
                            | 'default' ':' stat
                            ;
    EBNF:
    labeled_stat            : id ':' stat
                            | 'case' logical_or_exp ':' stat
                            | 'default' ':' stat
                            ;
    parse labeled statement.
    """

    @classmethod
    def parse(cls, token_source: TokenSource):
        """parse token source to recursively construct a node."""
        node = cls("labeled statement")

        if token_source.peek(1).type == 'ID':
            node.child.append(ParseToken.parse(token_source))
            if token_source.peek(1).value == ':':
                node.child.append(ParseToken.parse(token_source))
                node.child.append(ParseStatement.parse(token_source))
            else:
                raise ParseException("at %s, expect ':'" %
                                     (token_source.peek(1).cursor))
        elif token_source.peek(1).value == 'case':
            node.child.append(ParseToken.parse(token_source))
            node.child.append(ParseLogicalOrExp.parse(token_source))
            if token_source.peek(1).value == ':':
                node.child.append(ParseToken.parse(token_source))
                node.child.append(ParseStatement.parse(token_source))
            else:
                raise ParseException("at %s, expect ':'" %
                                     (token_source.peek(1).cursor))
        elif token_source.peek(1).value == 'default':
            node.child.append(ParseToken.parse(token_source))
            if token_source.peek(1).value == ':':
                node.child.append(ParseToken.parse(token_source))
                node.child.append(ParseStatement.parse(token_source))
            else:
                raise ParseException("at %s, expect ':'" %
                                     (token_source.peek(1).cursor))
        else:
            raise ParseException("at %s, expect labeled statement element." % (
                token_source.peek(1).cursor))

        return node


class ParseExpStat(ParseNode):
    """
    BNF:
    exp_stat                : exp ';'
                            |	';'
                            ;
    EBNF:
    exp_stat                : [ exp ] ';'
                            ;
    parse expression statement.
    """

    @classmethod
    def parse(cls, token_source: TokenSource):
        """parse token source to recursively construct a node."""
        node = cls("expression statement")

        if token_source.peek(1).type in ('ID', 'VAL') or token_source.peek(1).value in ('(', '+', '-', '!', '++', '--'):
            node.child.append(ParseExpression.parse(token_source))
        if token_source.peek(1).value == ';':
            node.child.append(ParseToken.parse(token_source))
        else:
            raise ParseException("at %s, '%s' is not ';', expect ';'" % (
                token_source.peek(1).cursor,
                token_source.peek(1).value))

        return node


class ParseCompoundStat(ParseNode):
    """
    BNF:
    compound_stat           : '{' decl_list stat_list '}'
                            | '{'		stat_list '}'
                            | '{' decl_list		'}'
                            | '{'			'}'
                            ;
    EBNF:
    compound_stat           : '{' [ decl_list ] [ stat_list ] '}'
                            ;
    parse compound statement.
    """

    @classmethod
    def parse(cls, token_source: TokenSource):
        """parse token source to recursively construct a node."""
        node = cls("compound statement")

        if token_source.peek(1).value == '{':
            node.child.append(ParseToken.parse(token_source))
            if token_source.peek(1).value in var_types:
                node.child.append(ParseDeclList.parse(token_source))
            if ParseStatement.is_stat(token_source):
                node.child.append(ParseStatList.parse(token_source))
            if token_source.peek(1).value == '}':
                node.child.append(ParseToken.parse(token_source))
            else:
                raise ParseException("at %s, expect '}'" %
                                     (token_source.peek(1).cursor))
        else:
            raise ParseException("at %s expect '{'" % (
                token_source.peek(1).cursor))

        return node


class ParseStatList(ParseNode):
    """
    BNF:
    stat_list               : stat
                            | stat_list stat
                            ;
    EBNF:
    stat_list               : stat { stat }
                            ;
    parse statement list.
    """

    @classmethod
    def parse(cls, token_source: TokenSource):
        """parse token source to recursively construct a node."""
        node = cls("statement list")

        node.child.append(ParseStatement.parse(token_source))
        while ParseStatement.is_stat(token_source):
            node.child.append(ParseStatement.parse(token_source))

        return node


class ParseSelectionStat(ParseNode):
    """
    BNF:
    selection_stat          : 'if' '(' exp ')' stat
                            | 'if' '(' exp ')' stat 'else' stat
                            | 'switch' '(' exp ')' stat
                            ;
    EBNF:
    selection_stat          : 'if' '(' exp ')' stat [ 'else' stat ]
                            | 'switch' '(' exp ')' stat
                            ;
    parse selection statement.
    """

    @classmethod
    def parse(cls, token_source: TokenSource):
        """parse token source to recursively construct a node."""
        node = cls("selection statement")

        if token_source.peek(1).value == 'if':
            node.child.append(ParseToken.parse(token_source))
            if token_source.peek(1).value == '(':
                node.child.append(ParseToken.parse(token_source))
                node.child.append(ParseExpression.parse(token_source))
                if token_source.peek(1).value == ')':
                    node.child.append(ParseToken.parse(token_source))
                    node.child.append(ParseStatement.parse(token_source))
                    if token_source.peek(1).value == 'else':
                        node.child.append(ParseToken.parse(token_source))
                        node.child.append(ParseStatement.parse(token_source))
                else:
                    raise ParseException("at %s, expect ')'." %
                                         (token_source.peek(1).cursor))
            else:
                raise ParseException("at %s, expect '('." %
                                     (token_source.peek(1).cursor))
        elif token_source.peek(1).value == 'switch':
            node.child.append(ParseToken.parse(token_source))
            if token_source.peek(1).value == '(':
                node.child.append(ParseToken.parse(token_source))
                node.child.append(ParseExpression.parse(token_source))
                if token_source.peek(1).value == ')':
                    node.child.append(ParseToken.parse(token_source))
                    node.child.append(ParseStatement.parse(token_source))
                else:
                    raise ParseException("at %s, expect ')'." %
                                         (token_source.peek(1).cursor))
            else:
                raise ParseException("at %s, expect '('." %
                                     (token_source.peek(1).cursor))
        else:
            raise ParseException("at %s, expect selection statement." % (
                token_source.peek(1).cursor))

        return node


class ParseIterationStat(ParseNode):
    """
    BNF:
    iteration_stat          : 'while' '(' exp ')' stat
                            | 'do' stat 'while' '(' exp ')' ';'
                            ;
    EBNF:
    iteration_stat          : 'while' '(' exp ')' stat
                            | 'do' stat 'while' '(' exp ')' ';'
                            ;
    parse iteration statement.
    """

    @classmethod
    def parse(cls, token_source: TokenSource):
        """parse token source to recursively construct a node."""
        node = cls("iteration statement")

        if token_source.peek(1).value == 'while':
            node.child.append(ParseToken.parse(token_source))
            if token_source.peek(1).value == '(':
                node.child.append(ParseToken.parse(token_source))
                node.child.append(ParseExpression.parse(token_source))
                if token_source.peek(1).value == ')':
                    node.child.append(ParseToken.parse(token_source))
                    node.child.append(ParseStatement.parse(token_source))
                else:
                    raise ParseException("at %s, expect ')'." %
                                         (token_source.peek(1).cursor))
            else:
                raise ParseException("at %s, expect '('." %
                                     (token_source.peek(1).cursor))
        elif token_source.peek(1).value == 'do':
            node.child.append(ParseToken.parse(token_source))
            node.child.append(ParseStatement.parse(token_source))
            if token_source.peek(1).value == 'while':
                node.child.append(ParseToken.parse(token_source))
                if token_source.peek(1).value == '(':
                    node.child.append(ParseToken.parse(token_source))
                    node.child.append(ParseExpression.parse(token_source))
                    if token_source.peek(1).value == ')':
                        node.child.append(ParseToken.parse(token_source))
                        if token_source.peek(1).value == ';':
                            node.child.append(ParseToken.parse(token_source))
                        else:
                            raise ParseException("at %s, expect ';'." % (
                                token_source.peek(1).cursor))
                    else:
                        raise ParseException("at %s, expect ')'." % (
                            token_source.peek(1).cursor))
                else:
                    raise ParseException(
                        "at %s, expect '('." % (token_source.peek(1).cursor))
            else:
                raise ParseException("at %s, expect 'while'." %
                                     (token_source.peek(1).cursor))
        else:
            raise ParseException("at %s, expect iteration statement." % (
                token_source.peek(1).cursor))

        return node


class ParseJumpStat(ParseNode):
    """
    BNF:
    jump_stat               : 'continue' ';'
                            | 'break' ';'
                            | 'return' exp ';'
                            | 'return'	';'
                            ;
    EBNF:
    jump_stat               : 'continue' ';'
                            | 'break' ';'
                            | 'return' [ exp ] ';'
                            ;
    parse jump statement.
    """

    @classmethod
    def parse(cls, token_source: TokenSource):
        """parse token source to recursively construct a node."""
        node = cls("jump statement")

        if token_source.peek(1).value == 'continue':
            node.child.append(ParseToken.parse(token_source))
            if token_source.peek(1).value == ';':
                node.child.append(ParseToken.parse(token_source))
            else:
                raise ParseException("at %s, expect ';'." %
                                     (token_source.peek(1).cursor))
        elif token_source.peek(1).value == 'break':
            node.child.append(ParseToken.parse(token_source))
            if token_source.peek(1).value == ';':
                node.child.append(ParseToken.parse(token_source))
            else:
                raise ParseException("at %s, expect ';'." %
                                     (token_source.peek(1).cursor))
        elif token_source.peek(1).value == 'return':
            node.child.append(ParseToken.parse(token_source))
            if token_source.peek(1).type in ('ID', 'VAL') or token_source.peek(1).value in ('(', '+', '-', '!', '++', '--'):
                node.child.append(ParseExpression.parse(token_source))
            if token_source.peek(1).value == ';':
                node.child.append(ParseToken.parse(token_source))
            else:
                raise ParseException("at %s, '%s' is not ';', expect ';'" % (
                    token_source.peek(1).cursor,
                    token_source.peek(1).value))

        return node


class ParseExpression(ParseNode):
    """
    BNF:
    exp                     : assignment_exp
                            | exp ',' assignment_exp
                            ;
    EBNF:
    exp                     : assignment_exp { ',' assignment_exp }
                            ;
    parse expression.
    """

    @classmethod
    def parse(cls, token_source: TokenSource):
        """parse token source to recursively construct a node."""
        node = cls("expression")

        node.child.append(ParseAssignmentExp.parse(token_source))
        while token_source.peek(1).value == ',':
            node.child.append(ParseToken.parse(token_source))
            node.child.append(ParseAssignmentExp.parse(token_source))

        return node


class ParseAssignmentExp(ParseNode):
    """
    BNF:
    assignment_exp          : logical_or_exp
                            | unary_exp assignment_operator assignment_exp
                            ;
    EBNF:
    assignment_exp          : { unary_exp assignment_operator } logical_or_exp
                            ;
    parse assignment expression.
    """

    @classmethod
    def parse(cls, token_source: TokenSource):
        """parse token source to recursively construct a node."""
        node = cls("assignment expression")

        while (token_source.peek(1).type in ('ID', 'VAL') or token_source.peek(1).value in ('(', '+', '-', '!', '++', '--')) and token_source.peek(2).value in ('=', '*=', '/=', '+=', '-='):
            node.child.append(ParseUnaryExp.parse(token_source))
            node.child.append(ParseAssignmentOperator.parse(token_source))
        node.child.append(ParseLogicalOrExp.parse(token_source))

        return node


class ParseAssignmentOperator(ParseNode):
    """
    BNF:
    assignment_operator     : '=' | '*=' | '/=' | '+=' | '-='
                            ;
    EBNF:
    assignment_operator     : '=' | '*=' | '/=' | '+=' | '-='
                            ;
    parse assignment expression.
    """

    @staticmethod
    def is_assignment_operator(token_source):
        """check if next token is a assignment operator"""
        return token_source.peek(1).value in ('=', '*=', '/=', '+=', '-=')

    @classmethod
    def parse(cls, token_source: TokenSource):
        """parse token source to recursively construct a node."""
        if cls.is_assignment_operator(token_source):
            return cls(token_source.get())
        else:
            raise ParseException("at %s, '%s' is not an assignment operator, expect assignment operator" % (
                token_source.peek(1).cursor,
                token_source.peek(1).value))


class ParseLogicalOrExp(ParseNode):
    """
    BNF:
    logical_or_exp          : logical_and_exp
                            | logical_or_exp '||' logical_and_exp
                            ;
    EBNF:
    logical_or_exp          : logical_and_exp { '||' logical_and_exp }
                            ;
    parse logical or expression.
    """

    @classmethod
    def parse(cls, token_source: TokenSource):
        """parse token source to recursively construct a node."""
        node = cls("logical or expression")

        node.child.append(ParseLogicalAndExp.parse(token_source))
        while token_source.peek(1).value == '||':
            node.child.append(ParseToken.parse(token_source))
            node.child.append(ParseLogicalAndExp.parse(token_source))

        return node


class ParseLogicalAndExp(ParseNode):
    """
    BNF:
    logical_and_exp         : equality_exp
                            | logical_and_exp '&&' equality_exp
                            ;
    EBNF:
    logical_and_exp         : equality_exp { '&&' equality_exp }
                            ;
    parse logical and expression.
    """

    @classmethod
    def parse(cls, token_source: TokenSource):
        """parse token source to recursively construct a node."""
        node = cls("logical andr expression")

        node.child.append(ParseEqualityExp.parse(token_source))
        while token_source.peek(1).value == '&&':
            node.child.append(ParseToken.parse(token_source))
            node.child.append(ParseEqualityExp.parse(token_source))

        return node


class ParseEqualityExp(ParseNode):
    """
    BNF:
    equality_exp            : relational_exp
                            | equality_exp '==' relational_exp
                            | equality_exp '!=' relational_exp
                            ;
    EBNF:
    equality_exp            : relational_exp { '==' relational_exp | '!=' relational_exp }
                            ;
    parse equality expression.
    """

    @classmethod
    def parse(cls, token_source: TokenSource):
        """parse token source to recursively construct a node."""
        node = cls("equality expression")

        node.child.append(ParseRelationalExp.parse(token_source))
        while token_source.peek(1).value in ('!=', '=='):
            node.child.append(ParseToken.parse(token_source))
            node.child.append(ParseRelationalExp.parse(token_source))

        return node


class ParseRelationalExp(ParseNode):
    """
    BNF:
    relational_exp          : additive_exp
                            | relational_exp '<' additive_exp
                            | relational_exp '>' additive_exp
                            | relational_exp '<=' additive_exp
                            | relational_exp '>=' additive_exp
                            ;
    EBNF:
    relational_exp          : additive_exp { '<' additive_exp | '>' additive_exp | '<=' additive_exp | '>=' additive_exp }
                            ;
    parse relational expression.
    """

    @classmethod
    def parse(cls, token_source: TokenSource):
        """parse token source to recursively construct a node."""
        node = cls("relational expression")

        node.child.append(ParseAdditiveExp.parse(token_source))
        while token_source.peek(1).value in ('>', '<', '>=', '<='):
            node.child.append(ParseToken.parse(token_source))
            node.child.append(ParseAdditiveExp.parse(token_source))

        return node


class ParseAdditiveExp(ParseNode):
    """
    BNF:
    additive_exp            : mult_exp
                            | additive_exp '+' mult_exp
                            | additive_exp '-' mult_exp
                            ;
    EBNF:
    additive_exp            : mult_exp { '+' mult_exp | '-' mult_exp }
                            ;
    parse additive expression.
    """

    @classmethod
    def parse(cls, token_source: TokenSource):
        """parse token source to recursively construct a node."""
        node = cls("additive expression")

        node.child.append(ParseMultExp.parse(token_source))
        while token_source.peek(1).value in ('+', '-'):
            node.child.append(ParseToken.parse(token_source))
            node.child.append(ParseMultExp.parse(token_source))

        return node


class ParseMultExp(ParseNode):
    """
    BNF:
    mult_exp                : cast_exp
                            | mult_exp '*' cast_exp
                            | mult_exp '/' cast_exp
                            ;
    EBNF:
    mult_exp                : cast_exp { '*' cast_exp | '/' cast_exp }
                            ;
    parse multiple expression.
    """

    @classmethod
    def parse(cls, token_source: TokenSource):
        """parse token source to recursively construct a node."""
        node = cls("multiple expression")

        node.child.append(ParseCastExp.parse(token_source))
        while token_source.peek(1).value in ('*', '/'):
            node.child.append(ParseToken.parse(token_source))
            node.child.append(ParseCastExp.parse(token_source))

        return node


class ParseCastExp(ParseNode):
    """
    BNF:
    cast_exp                : unary_exp
                            | '(' type_spec ')' cast_exp
                            ;
    EBNF:
    cast_exp                : {'(' type_spec ')'} unary_exp
                            ;
    parse cast expression.
    """

    @classmethod
    def parse(cls, token_source: TokenSource):
        """parse token source to recursively construct a node."""
        node = cls("cast expression")

        while token_source.peek(1).value == '(':
            node.child.append(ParseToken.parse(token_source))
            node.child.append(ParseTypeSpec.parse(token_source))
            if token_source.peek(1).value == ')':
                node.child.append(ParseToken.parse(token_source))
            else:
                raise ParseException("at %s, expect ')'" %
                                     (token_source.peek(1).cursor))
        node.child.append(ParseUnaryExp.parse(token_source))

        return node


class ParseUnaryExp(ParseNode):
    """
    BNF:
    unary_exp               : postfix_exp
                            | '++' unary_exp
                            | '--' unary_exp
                            | unary_operator cast_exp
                            ;
    EBNF:
    unary_exp               : { '++' | '--' } ( postfix_exp | unary_operator cast_exp )
                            ;
    parse unary expression.
    """

    # TODO: fix semantic error.
    @classmethod
    def parse(cls, token_source: TokenSource):
        """parse token source to recursively construct a node."""
        node = cls("unary expression")

        while token_source.peek(1).value in ('++', '--'):
            node.child.append(ParseToken.parse(token_source))
        if token_source.peek(1).type in ('ID', 'VAL') or token_source.peek(1).value == '(':
            node.child.append(ParsePostfixExp.parse(token_source))
        elif token_source.peek(1).value in ('+', '-', '!'):
            node.child.append(ParseUnaryOperator.parse(token_source))
        else:
            raise ParseException("at %s, expect ID, unary operator or const value." %
                                    (token_source.peek(1).cursor))

        return node


class ParseUnaryOperator(ParseNode):
    """
    BNF:
    unary_operator          : '+' | '-' | '!'
                            ;
    EBNF:
    unary_operator          : '+' | '-' | '!'
                            ;
    parse unary operator.
    """

    @classmethod
    def parse(cls, token_source: TokenSource):
        """parse token source to recursively construct a node."""
        if token_source.peek(1).value in ('+', '-', '!'):
            return cls(token_source.get())
        else:
            raise ParseException("at %s, expect unary Operator." %
                                 (token_source.peek(1).cursor))


class ParsePostfixExp(ParseNode):
    """
    BNF:
    postfix_exp             : primary_exp
                            | postfix_exp '[' exp ']'
                            | postfix_exp '(' argument_exp_list ')'
                            | postfix_exp '('			')'
                            | postfix_exp '++'
                            | postfix_exp '--'
                            ;
    EBNF:
    postfix_exp             : primary_exp { '[' exp ']' |
                                            '(' [ argument_exp_list ] ')' |
                                            '++' |
                                            '--' }
                            ;
    parse postfix expression.
    """

    @classmethod
    def parse(cls, token_source: TokenSource):
        """parse token source to recursively construct a node."""
        node = cls("postfix expression")

        node.child.append(ParsePrimaryExp.parse(token_source))
        if token_source.peek(1).value == '[':
            node.child.append(ParseToken.parse(token_source))
            node.child.append(ParseExpression.parse(token_source))
            if token_source.peek(1).value == ']':
                node.child.append(ParseToken.parse(token_source))
            else:
                raise ParseException("at %s, '%s' is not ')', expect ')'" % (
                    token_source.peek(1).cursor))
        elif token_source.peek(1).value == '(':
            node.child.append(ParseToken.parse(token_source))
            if token_source.peek(1).type in ('ID', 'VAL') or token_source.peek(1).value in ('+', '-', '!', '(', '++', '--'):
                node.child.append(ParseArgumentExpList.parse(token_source))
            if token_source.peek(1).value == ')':
                node.child.append(ParseToken.parse(token_source))
            else:
                raise ParseException("at %s, '%s' is not ')', expect ')'" % (
                    token_source.peek(1).cursor))
        elif token_source.peek(1).value == '++':
            node.child.append(ParseToken.parse(token_source))
        elif token_source.peek(1).value == '--':
            node.child.append(ParseToken.parse(token_source))

        return node


class ParsePrimaryExp(ParseNode):
    """
    BNF:
    primary_exp             : id
                            | const
                            | string
                            | '(' exp ')'
                            ;
    EBNF:
    primary_exp             : id
                            | const
                            | string
                            | '(' exp ')'
                            ;
    parse primary expression.
    """

    @classmethod
    def parse(cls, token_source: TokenSource):
        """parse token source to recursively construct a node."""
        if token_source.peek(1).type in ('ID', 'VAL') or token_source.peek(1).value == '(':
            return cls(token_source.get())
        else:
            raise ParseException(
                "at %s, expect id, const value, string or '('" % (token_source.peek(1).cursor))


class ParseArgumentExpList(ParseNode):
    """
    BNF:
    argument_exp_list       : assignment_exp
                            | argument_exp_list ',' assignment_exp
                            ;
    EBNF:
    argument_exp_list       : assignment_exp { ',' assignment_exp }
                            ;
    parse argument expression.
    """

    @classmethod
    def parse(cls, token_source: TokenSource):
        """parse token source to recursively construct a node."""
        node = cls("argument expression")

        node.child.append(ParseAssignmentExp.parse(token_source))
        while token_source.peek(1).value == ',':
            node.child.append(ParseToken.parse(token_source))
            node.child.append(ParseAssignmentExp.parse(token_source))

        return node

# NOTE: I don't think I need the class below.
# class ParseConst(ParseNode):
#     """
#     BNF:
#     const                   : int_const
#                             | char_const
#                             | float_const
#                             ;
#     EBNF:
#     const                   : int_const
#                             | char_const
#                             | float_const
#                             ;
#     parse const.
#     """

#     def __init__(self):
#         super(ParseConst, self).__init__("const")

#     def parse(self, token_source: TokenSource):
#         pass
