"""
Asset mudule.
"""
keywords = ("if", "else", "then", "case", "while", "do", "break", "continue", "return", "switch", "default", "int", "float", "char", "bool")
var_types = ("int", "float", "char", "bool")
delimiters = (",", ";", ":", "(", ")", "[", "]", "{", "}")
operators = ("+", "-", "*", "/", "<", "=", ">", "&", "|", "!")

terminators = ('int_const', 'char_const', 'float_const', 'id', 'string')


BNF = [
    ('translation_unit',     ['external_decl',
                              'translation_unit' 'external_decl']),

    ('external_decl',        ['function_definition',
                              'decl']),

    ('function_definition',  ['decl_specs' 'declarator' 'decl_list' 'compound_stat',
                              'declarator' 'decl_list' 'compound_stat',
                              'decl_specs' 'declarator' 'compound_stat',
                              'declarator' 'compound_stat']),

    ('decl',                 ['decl_specs' 'init_declarator_list' ';',
                              'decl_specs'			';']),

    ('decl_list',            ['decl',
                              'decl_list' 'decl']),

    ('decl_specs',           ['type_spec' 'decl_specs',
                              'type_spec']),

    ('type_spec',            ['char' | 'int' | 'bool' | 'float']),

    ('init_declarator_list', ['init_declarator',
                              'init_declarator_list' ',' 'init_declarator']),

    ('init_declarator',      ['declarator',
                              'declarator' '=' 'initializer']),

    ('spec_qualifier_list',  ['type_spec' 'spec_qualifier_list',
                              'type_spec']),

    ('declarator',           ['id',
                              'declarator' '[' 'logical_or_exp' ']',
                              'declarator' '['		']',
                              'declarator' '(' 'param_list' ')',
                              'declarator' '(' 'id_list' ')',
                              'declarator' '('		')']),

    ('param_list',           ['param_decl',
                              'param_list' ',' 'param_decl']),

    ('param_decl',           ['decl_specs' 'declarator',
                              'decl_specs']),

    ('id_list',              ['id',
                              'id_list' ',' 'id']),

    ('initializer',          ['assignment_exp',
                              '{' 'initializer_list' '}',
                              '{' 'initializer_list' ',' '}']),

    ('initializer_list',     ['initializer',
                              'initializer_list' ',' 'initializer']),

    ('stat',                 ['labeled_stat',
                              'exp_stat',
                              'compound_stat',
                              'selection_stat',
                              'iteration_stat',
                              'jump_stat']),

    ('labeled_stat',         ['id' ':' 'stat',
                              'case' 'logical_or_exp' ':' 'stat',
                              'default' ':' 'stat']),

    ('exp_stat',             ['exp' ';',
                              ';']),

    ('compound_stat',        ['{' 'decl_list' 'stat_list' '}',
                              '{'		'stat_list' '}',
                              '{' 'decl_list'		'}',
                              '{'			'}']),

    ('stat_list',            ['stat',
                              'stat_list' 'stat']),

    ('selection_stat',       ['if' '(' 'exp' ')' 'stat',
                              'if' '(' 'exp' ')' 'stat' 'else' 'stat',
                              'switch' '(' 'exp' ')' 'stat']),

    ('iteration_stat',       ['while' '(' 'exp' ')' 'stat',
                              'do' 'stat' 'while' '(' 'exp' ')' ';']),

    ('jump_stat',            ['continue' ';',
                              'break' ';',
                              'return' 'exp' ';',
                              'return'	';']),

    ('exp',                  ['assignment_exp',
                              'exp' ',' 'assignment_exp']),

    ('assignment_exp',       ['conditional_exp',
                              'unary_exp' 'assignment_operator' 'assignment_exp']),

    ('assignment_operator',  ['=', '*=', '/=', '+=', '-=']),

    ('logical_or_exp',       ['logical_and_exp',
                              'logical_or_exp' '||' 'logical_and_exp']),

    ('logical_and_exp',      ['equality_exp',
                              'logical_and_exp' '&&' 'equality_exp']),

    ('equality_exp',         ['relational_exp',
                              'equality_exp' '==' 'relational_exp',
                              'equality_exp' '!=' 'relational_exp']),

    ('relational_exp',       ['additive_exp',
                              'relational_exp' '<' 'additive_exp',
                              'relational_exp' '>' 'additive_exp',
                              'relational_exp' '<=' 'additive_exp',
                              'relational_exp' '>=' 'additive_exp']),

    ('additive_exp',         ['mult_exp',
                              'additive_exp' '+' 'mult_exp',
                              'additive_exp' '-' 'mult_exp']),

    ('mult_exp',             ['cast_exp',
                              'mult_exp' '*' 'cast_exp',
                              'mult_exp' '/' 'cast_exp']),

    ('cast_exp',             ['unary_exp',
                              '(' 'spec_qualifier_list' ')' 'cast_exp']),

    ('unary_exp',            ['postfix_exp',
                              '++' 'unary_exp',
                              '--' 'unary_exp',
                              'unary_operator' 'cast_exp']),

    ('unary_operator',       ['+', '-', '!']),

    ('postfix_exp',          ['primary_exp',
                              'postfix_exp' '[' 'exp' ']',
                              'postfix_exp' '(' 'argument_exp_list' ')',
                              'postfix_exp' '('			')',
                              'postfix_exp' '++',
                              'postfix_exp' '--']),

    ('primary_exp',          ['id',
                              'const',
                              'string',
                              '(' 'exp' ')']),

    ('argument_exp_list',    ['assignment_exp',
                              'argument_exp_list' ',' 'assignment_exp']),

    ('const',                ['int_const',
                              'char_const',
                              'float_const']),

]
