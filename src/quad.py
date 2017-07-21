"""
travel AST and generate quad, contians several visitor.
"""
import src.ast as ast
from symbol_table import SymbolTable
from src.token import TokenType


class ASTVisitor(object):
    """base abstrace class of Visitors"""

    def semantic_analyze(self, ast_node: ast.AbstractSyntaxTreeNode):
        """double dispatch method"""
        if isinstance(ast_node, ast.SourceRoot):
            self._init_declarator_list(ast_node)
        elif isinstance(ast_node, ast.ExternalDecl):
            self._init_declarator_list(ast_node)
        elif isinstance(ast_node, ast.InitDeclaratorList):
            self._init_declarator_list(ast_node)
        elif isinstance(ast_node, ast.InitDeclarator):
            self._init_declarator(ast_node)
        elif isinstance(ast_node, ast.VarDeclarator):
            self._var_declarator(ast_node)
        elif isinstance(ast_node, ast.Initializer):
            self._initializer(ast_node)
        elif isinstance(ast_node, ast.FunctionDefinition):
            self._function_defination(ast_node)
        elif isinstance(ast_node, ast.ParamList):
            self._param_list(ast_node)
        elif isinstance(ast_node, ast.ParamDecl):
            self._param_decl(ast_node)
        elif isinstance(ast_node, ast.LocalDeclList):
            self._local_decl_list(ast_node)
        elif isinstance(ast_node, ast.CompoundStat):
            self._compound_stat(ast_node)
        elif isinstance(ast_node, ast.LabeledStat):
            self._labeled_stat(ast_node)
        elif isinstance(ast_node, ast.ExpStat):
            self._exp_stat(ast_node)
        elif isinstance(ast_node, ast.SelectionStat):
            self._selection_stat(ast_node)
        elif isinstance(ast_node, ast.IterationStat):
            self._iteration_stat(ast_node)
        elif isinstance(ast_node, ast.JumpStat):
            self._jump_stat(ast_node)
        elif isinstance(ast_node, ast.Expression):
            self._comma_exp(ast_node)
        elif isinstance(ast_node, ast.LogicalOrExp):
            self._logical_or_exp(ast_node)
        elif isinstance(ast_node, ast.LogicalAndExp):
            self._logical_and_exp(ast_node)
        elif isinstance(ast_node, ast.EqualityExp):
            self._equality_exp(ast_node)
        elif isinstance(ast_node, ast.RelationalExp):
            self._relational_exp(ast_node)
        elif isinstance(ast_node, ast.AdditiveExp):
            self._additive_exp(ast_node)
        elif isinstance(ast_node, ast.MultExp):
            self._mult_exp(ast_node)
        elif isinstance(ast_node, ast.CastExp):
            self._cast_exp(ast_node)
        elif isinstance(ast_node, ast.PostfixExp):
            self._postfix_exp(ast_node)
        elif isinstance(ast_node, ast.PrimaryExp):
            self._primary_exp(ast_node)
        else:
            pass

    def _source_root(self, ast_node: ast.AbstractSyntaxTreeNode):
        raise NotImplementedError

    def _external_decl(self, ast_node: ast.AbstractSyntaxTreeNode):
        raise NotImplementedError

    def _init_declarator_list(self, ast_node: ast.AbstractSyntaxTreeNode):
        raise NotImplementedError

    def _init_declarator(self, ast_node: ast.AbstractSyntaxTreeNode):
        raise NotImplementedError

    def _var_declarator(self, ast_node: ast.AbstractSyntaxTreeNode):
        raise NotImplementedError

    def _initializer(self, ast_node: ast.AbstractSyntaxTreeNode):
        raise NotImplementedError

    def _function_defination(self, ast_node: ast.AbstractSyntaxTreeNode):
        raise NotImplementedError

    def _stat_list(self, ast_node: ast.AbstractSyntaxTreeNode):
        raise NotImplementedError

    def _param_list(self, ast_node: ast.AbstractSyntaxTreeNode):
        raise NotImplementedError

    def _param_decl(self, ast_node: ast.AbstractSyntaxTreeNode):
        raise NotImplementedError

    def _local_decl_list(self, ast_node: ast.AbstractSyntaxTreeNode):
        raise NotImplementedError

    def _compound_stat(self, ast_node: ast.AbstractSyntaxTreeNode):
        raise NotImplementedError

    def _labeled_stat(self, ast_node: ast.AbstractSyntaxTreeNode):
        raise NotImplementedError

    def _exp_stat(self, ast_node: ast.AbstractSyntaxTreeNode):
        raise NotImplementedError

    def _selection_stat(self, ast_node: ast.AbstractSyntaxTreeNode):
        raise NotImplementedError

    def _iteration_stat(self, ast_node: ast.AbstractSyntaxTreeNode):
        raise NotImplementedError

    def _jump_stat(self, ast_node: ast.AbstractSyntaxTreeNode):
        raise NotImplementedError

    def _comma_exp(self, ast_node: ast.AbstractSyntaxTreeNode):
        raise NotImplementedError

    def _assignment_exp(self, ast_node: ast.AbstractSyntaxTreeNode):
        raise NotImplementedError

    def _logical_or_exp(self, ast_node: ast.AbstractSyntaxTreeNode):
        raise NotImplementedError

    def _logical_and_exp(self, ast_node: ast.AbstractSyntaxTreeNode):
        raise NotImplementedError

    def _equality_exp(self, ast_node: ast.AbstractSyntaxTreeNode):
        raise NotImplementedError

    def _relational_exp(self, ast_node: ast.AbstractSyntaxTreeNode):
        raise NotImplementedError

    def _additive_exp(self, ast_node: ast.AbstractSyntaxTreeNode):
        raise NotImplementedError

    def _mult_exp(self, ast_node: ast.AbstractSyntaxTreeNode):
        raise NotImplementedError

    def _cast_exp(self, ast_node: ast.AbstractSyntaxTreeNode):
        raise NotImplementedError

    def _unary_exp(self, ast_node: ast.AbstractSyntaxTreeNode):
        raise NotImplementedError

    def _postfix_exp(self, ast_node: ast.AbstractSyntaxTreeNode):
        raise NotImplementedError

    def _primary_exp(self, ast_node: ast.AbstractSyntaxTreeNode):
        raise NotImplementedError


class AttrCalculateVisitor(ASTVisitor):
    """visitor for calculate attribute"""

    def __init__(self, symbol_table: SymbolTable):
        self.symbol_table: SymbolTable = symbol_table

    def _source_root(self, ast_node):
        ast_node.scope = "global"
        for external_decl in ast_node.child:
            external_decl.accept(self)

    def _external_decl(self, ast_node):
        ast_node.scope = ast_node.father_node.scope
        ast.child[0].accept(self)

    def _init_declarator_list(self, ast_node):
        var_type = ast_node.child[0].symbol.value
        ast_node.type = var_type
        ast_node.scope = ast_node.father_node.scope
        for init_declarator in ast_node.child[1:]:
            init_declarator.accept(self)

    def _init_declarator(self, ast_node):
        ast_node.type = ast_node.father_node.type
        ast_node.scope = ast_node.father_node.scope
        for child in ast_node.child:
            child.accept(self)
        ast_node.value = ast_node.child[1].value

    def _var_declarator(self, ast_node):
        ast_node.type = ast_node.father_node.type
        ast_node.scope = ast_node.father_node.scope
        if ast_node.child:
            ast_node.child[1].accept(self)
            ast_node.array_dimension = (ast_node.child[0], ) + ast_node.child[1].array_dimension
        else:
            self.symbol_table.create_item(ast_node.symbol.value, ast_node.type, ast_node.scope)
        # TODO: finish this.
    def _initializer(self, ast_node):
        pass


class TypeCheckingVisitor(ASTVisitor):
    """visitor for check type"""

    def __init__(self, symbol_table: SymbolTable):
        self.symbol_table: SymbolTable = symbol_table

    # def type_check(self, var_type):
    #     """return enum value of var type"""
    #     if var_type == "int":
    #         return TokenType.INT_CONST

    # def _init_declarator_list(self, ast_node):
    #     var_type = ast_node.child[0].symbol.value
    #     for init_declarator in ast_node.child[1:]:
    #         if init_declarator.child:
    # TODO: implement type check.


class QuadGeneratingVisitor(ASTVisitor):
    """visitor for generate quad"""

    def __init__(self, symbol_table: SymbolTable):
        self.symbol_table: SymbolTable = symbol_table

    def _init_declarator_list(self, ast_node):
        var_type = ast_node.child[0].symbol.value
        ast_node.type = var_type

    def _init_declarator(self, ast_node):
        ast_node.type = ast_node.father_node.type

    def _var_declarator(self, ast_node):
        ast_node.type = ast_node.father_node.type
        self.symbol_table.create_item(ast_node.symbol.value)

