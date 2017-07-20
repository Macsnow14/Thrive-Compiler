"""
travel AST and generate quad, contians several visitor.
"""
import src.ast as ast


class ASTVisitor(object):
    """base abstrace class of Visitors"""

    def semantic_analyze(self, ast_node: ast.AbstractSyntaxTreeNode):
        """double dispatch method"""
        if isinstance(ast_node, ast.InitDeclaratorList):
            self._init_declarator_list(ast_node)
        elif isinstance(ast_node, ast.InitDeclarator):
            self._init_declarator(ast_node)
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

    def _init_declarator_list(self, ast_node: ast.AbstractSyntaxTreeNode):
        raise NotImplementedError

    def _init_declarator(self, ast_node: ast.AbstractSyntaxTreeNode):
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
