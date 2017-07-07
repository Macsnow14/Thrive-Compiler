"""
paser to generate quaternary.

Recursive descent parsing.
"""
import json
from typing import List
from .token import Token


def parseDict(AST):
    """
    parse AST to dict obj.
    """
    return {'symbol': AST.token,
            'child': [parseDict(node) for node in AST.child if AST.child]}


class ParseNode(object):
    """
    Abstract Syntex Tree base class
    """

    def __init__(self, token: Token):
        self.token: Token = token
        self.child: List[Token] = list()

    def parse(self, token_source):
        raise NotImplementedError

    def __str__(self):
        return json.dumps(parseDict(self), indent=2)


class ParsetranslationUnit(ParseNode):
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

    def __init__(self):
        super(ParsetranslationUnit, self).__init__('translation Unit')

    def parse(self, token_source):
        if token_source.judge():
            pass


class ParseExternalDecl(ParseNode):
    """
    BNF:
    external_decl       : function_definition
                        | decl
                        ;
    EBNF:
    external_decl       : function_definition
                        | decl
                        ;

    parse external declaration.
    """

    def __init__(self):
        super(ParseExternalDecl, self).__init__('external declaration')

    def parse(self, token_source):
        pass


class ParseFunctionDefinition(ParseNode):
    """
    BNF:
    function_definition : decl_specs declarator decl_list compound_stat
                        |		declarator decl_list compound_stat
                        | decl_specs declarator		compound_stat
                        |		declarator 	compound_stat
                        ;
    EBNF:
    function_definition : [ decl_specs ] declarator [ decl_list ] compound_stat
                        ;

    parse function definition.
    """

    def __init__(self):
        super(ParseFunctionDefinition, self).__init__('function definition')

    def parse(self, token_source):
        pass


class ParseDecl(ParseNode):
    """
    BNF:
    decl		        : decl_specs init_declarator_list ';'
                        | decl_specs			';'
                        ;
    EBNF:
    decl		        : decl_specs [ init_declarator_list ] ';'
                        ;

    parse declaration.
    """

    def __init__(self):
        super(ParseDecl, self).__init__('declaration')

    def parse(self, token_source):
        pass


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

    def __init__(self):
        super(ParseDeclList, self).__init__("declaration list")

    def parse(self, token_source):
        pass


class ParseDeclSpecs(ParseNode):
    """
    BNF:
    decl_specs		        : type_spec decl_specs
                            | type_spec
                            ;
    EBNF:
    decl_specs		        : type_spec { type_spec }
                            ;

    parse declaration specs.
    """

    def __init__(self):
        super(ParseDeclSpecs, self).__init__("declaration specs")

    def parse(self, token_source):
        pass


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

    def __init__(self):
        super(ParseTypeSpec, self).__init__("type spec")

    def parse(self, token_source):
        pass


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

    def __init__(self):
        super(ParseInitDeclaratorList, self).__init__("init declarator list")

    def parse(self, token_source):
        pass


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

    def __init__(self):
        super(ParseInitDeclarator, self).__init__("init declarator")

    def parse(self, token_source):
        pass


class ParseSpecQualifierList(ParseNode):
    """
    BNF:
    spec_qualifier_list     : type_spec spec_qualifier_list
                            | type_spec
                            ;
    EBNF:
    spec_qualifier_list     : type_spec { type_spec }
                            ;

    parse spec qualifier list.
    """

    def __init__(self):
        super(ParseSpecQualifierList, self).__init__("spec qualifier list")

    def parse(self, token_source):
        pass


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
    declarator              : id { '[' logical_or_exp ']' }
                            | id { '['		']' }
                            | id { '(' param_list ')' }
                            | id { '(' id_list ')' }
                            | id { '('		')' }
                            ;

    parse declarator.
    """

    def __init__(self):
        super(ParseDeclarator, self).__init__("declarator")

    def parse(self, token_source):
        pass


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

    def __init__(self):
        super(ParseParamList, self).__init__("param list")

    def parse(self, token_source):
        pass


class ParseParamDecl(ParseNode):
    """
    BNF:
    param_decl              : decl_specs declarator
                            | decl_specs
                            ;
    EBNF:
    param_decl              : decl_specs { declarator }
                            ;

    parse param decl.
    """

    def __init__(self):
        super(ParseParamDecl, self).__init__("param decl")

    def parse(self, token_source):
        pass


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

    def __init__(self):
        super(ParseIdList, self).__init__("Id list")

    def parse(self, token_source):
        pass


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

    def __init__(self):
        super(ParseInitializer, self).__init__("initializer")

    def parse(self, token_source):
        pass


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

    def __init__(self):
        super(ParseInitializerList, self).__init__("initializer list")

    def parse(self, token_source):
        pass


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

    def __init__(self):
        super(ParseStatement, self).__init__("statement")

    def parse(self, token_source):
        pass


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

    def __init__(self):
        super(ParseLabeledStat, self).__init__("labeled statement")

    def parse(self, token_source):
        pass


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

    def __init__(self):
        super(ParseExpStat, self).__init__("expression statement")

    def parse(self, token_source):
        pass


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

    def __init__(self):
        super(ParseCompoundStat, self).__init__("compound statement")

    def parse(self, token_source):
        pass



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

    def __init__(self):
        super(ParseStatList, self).__init__("statement list")

    def parse(self, token_source):
        pass


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

    def __init__(self):
        super(ParseSelectionStat, self).__init__("selection statement")

    def parse(self, token_source):
        pass


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

    def __init__(self):
        super(ParseIterationStat, self).__init__("iteration statement")

    def parse(self, token_source):
        pass


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

    def __init__(self):
        super(ParseJumpStat, self).__init__("jump statement")

    def parse(self, token_source):
        pass


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

    def __init__(self):
        super(ParseExpression, self).__init__("expression")

    def parse(self, token_source):
        pass


class ParseAssignmentExp(ParseNode):
    """
    BNF:
    assignment_exp          : conditional_exp
                            | unary_exp assignment_operator assignment_exp
                            ;
    EBNF:
    assignment_exp          : { unary_exp assignment_operator } conditional_exp
                            ;
    parse assignment expression.
    """

    def __init__(self):
        super(ParseAssignmentExp, self).__init__("assignment expression")

    def parse(self, token_source):
        pass


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

    def __init__(self):
        super(ParseAssignmentOperator, self).__init__("assignment operator")

    def parse(self, token_source):
        pass


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

    def __init__(self):
        super(ParseLogicalOrExp, self).__init__("logical or expression")

    def parse(self, token_source):
        pass


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

    def __init__(self):
        super(ParseLogicalAndExp, self).__init__("logical and expression")

    def parse(self, token_source):
        pass


class ParseEqualityExp(ParseNode):
    """
    BNF:
    equality_exp            : relational_exp
                            | equality_exp '==' relational_exp
                            | equality_exp '!=' relational_exp
                            ;
    EBNF:
    equality_exp            : relational_exp { '==' relational_exp }
                            | relational_exp { '!=' relational_exp }
                            ;
    parse equality expression.
    """

    def __init__(self):
        super(ParseEqualityExp, self).__init__("equality expression")

    def parse(self, token_source):
        pass


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
    relational_exp          : additive_exp { '<' additive_exp }
                            | additive_exp { '>' additive_exp }
                            | additive_exp { '<=' additive_exp }
                            | additive_exp { '>=' additive_exp }
                            ;
    parse relational expression.
    """

    def __init__(self):
        super(ParseRelationalExp, self).__init__("relational expression")

    def parse(self, token_source):
        pass


class ParseAdditiveExp(ParseNode):
    """
    BNF:
    additive_exp            : mult_exp
                            | additive_exp '+' mult_exp
                            | additive_exp '-' mult_exp
                            ;
    EBNF:
    additive_exp            : mult_exp '+' mult_exp
                            | mult_exp '-' mult_exp
                            ;
    parse additive expression.
    """

    def __init__(self):
        super(ParseAdditiveExp, self).__init__("additive expression")

    def parse(self, token_source):
        pass


class ParseMultExp(ParseNode):
    """
    BNF:
    mult_exp                : cast_exp
                            | mult_exp '*' cast_exp
                            | mult_exp '/' cast_exp
                            ;
    EBNF:
    mult_exp                : cast_exp { '*' cast_exp }
                            | cast_exp { '/' cast_exp }
                            ;
    parse multiple expression.
    """

    def __init__(self):
        super(ParseMultExp, self).__init__("multiple expression")

    def parse(self, token_source):
        pass


class ParseCastExp(ParseNode):
    """
    BNF:
    cast_exp                : unary_exp
                            | '(' spec_qualifier_list ')' cast_exp
                            ;
    EBNF:
    cast_exp                : {'(' spec_qualifier_list ')'} unary_exp
                            ;
    parse cast expression.
    """

    def __init__(self):
        super(ParseCastExp, self).__init__("cast expression")

    def parse(self, token_source):
        pass


class ParseUnaryExp(ParseNode):
    """
    BNF:
    unary_exp               : postfix_exp
                            | '++' unary_exp
                            | '--' unary_exp
                            | unary_operator cast_exp
                            ;
    EBNF:
    unary_exp               : { '++' } postfix_exp
                            | { '--' } postfix_exp
                            | { '++' } unary_operator cast_exp
                            | { '--' } unary_operator cast_exp
                            ;
    parse unary expression.
    """

    def __init__(self):
        super(ParseUnaryExp, self).__init__("unary expression")

    def parse(self, token_source):
        pass


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

    def __init__(self):
        super(ParseUnaryOperator, self).__init__("unary operator")

    def parse(self, token_source):
        pass


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
    postfix_exp             : primary_exp { '[' exp ']' }
                            | primary_exp { '(' argument_exp_list ')' }
                            | primary_exp { '('			')' }
                            | primary_exp { '++' }
                            | primary_exp { '--' }
                            ;
    parse postfix expression.
    """

    def __init__(self):
        super(ParsePostfixExp, self).__init__("postfix expression")

    def parse(self, token_source):
        pass


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

    def __init__(self):
        super(ParsePrimaryExp, self).__init__("primary expression")

    def parse(self, token_source):
        pass


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

    def __init__(self):
        super(ParseArgumentExpList, self).__init__("argument expression")

    def parse(self, token_source):
        pass

class ParseConst(ParseNode):
    """
    BNF:
    const                   : int_const
                            | char_const
                            | float_const
                            ;
    EBNF:
    const                   : int_const
                            | char_const
                            | float_const
                            ;
    parse const.
    """

    def __init__(self):
        super(ParseConst, self).__init__("const")

    def parse(self, token_source):
        pass
