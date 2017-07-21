"""
Transform a concrete syntax tree(CST) to a abstract syntax tree(AST)
Base assumption:
    CST is valid.

[AST structure form](http://www.cs.xu.edu/csci310/09s/ast.html)
"""
# NOTE: semantic analyze by travel ast.
# TODO: make each kind of node unique.

from typing import List
from .parser import ParseNode
from .token import Token
from .exceptions import TransformException


class AbstractSyntaxTreeNode(ParseNode):
    """base class node for AST with method for visitor"""

    def __init__(self, symbol: Token or str, father_node):
        self.symbol: Token or str = symbol
        self.child: List[ParseNode] = list()
        self.father_node = father_node

    def accept(self, visitor):
        """accept method for different visitor"""
        visitor.semantic_analyze(self)


class SourceRoot(AbstractSyntaxTreeNode):

    @classmethod
    def transform(cls, cst_node):
        ast_node = cls("source root", None)

        if cst_node.symbol == "translation Unit":
            for node in cst_node.child:
                ast_node.child.append(ExternalDecl.transform(node, ast_node))
        else:
            raise TransformException("expect a translation Unit node as the root of AST.")

        return ast_node


class ExternalDecl(AbstractSyntaxTreeNode):

    @classmethod
    def transform(cls, cst_node, father_node):
        ast_node = cls("external declaration", father_node)

        if cst_node.child[1].symbol == "init declarator list":
            ast_node.child.append(InitDeclaratorList.transform(cst_node.child[0], cst_node.child[1], ast_node))
        else:
            ast_node.child.append(FunctionDefinition.transform(cst_node.child[0], cst_node.child[1], ast_node))

        return ast_node


class InitDeclaratorList(AbstractSyntaxTreeNode):

    @classmethod
    def transform(cls, type_spec, cst_node, father_node):
        ast_node = cls("init declarator list", father_node)

        ast_node.child.append(type_spec)
        for node in cst_node.child:
            if node.symbol == "init declarator":
                ast_node.child.append(InitDeclarator.transform(node, ast_node))

        return ast_node


class InitDeclarator(AbstractSyntaxTreeNode):

    @classmethod
    def transform(cls, cst_node, father_node):
        if len(cst_node.child) > 1:
            ast_node = cls(cst_node.child[1].symbol, father_node)
            ast_node.child.append(VarDeclarator.transform(cst_node.child[0], ast_node))
            ast_node.child.append(Initializer.transform(cst_node.child[2], ast_node))
            return ast_node
        else:
            return VarDeclarator.transform(cst_node.child[0], father_node)


class Initializer(AbstractSyntaxTreeNode):

    @classmethod
    def transform(cls, cst_node, father_node):
        if isinstance(cst_node.child[0].symbol, Token) and cst_node.child[0].symbol == '{':
            return TransformException("array init are not support yet.")
        else:
            return AsignmentExp.transform(cst_node.child[0], father_node)


# class InitializerList(AbstractSyntaxTreeNode):

#     @classmethod
#     def transform(cls, cst_node, father_node):
#         pass


class VarDeclarator(AbstractSyntaxTreeNode):

    @classmethod
    def transform(cls, cst_node, father_node):
        if len(cst_node.child) > 1:
            ast_node = None
            if isinstance(cst_node.child[1].symbol, Token) and cst_node.child[1].symbol.value == "[":
                ast_node = cls("array decl", father_node)
                cst_node.child.pop(-1)
                ast_node.child.append(LogicalOrExp.transform(cst_node.child.pop(-1), ast_node))
                cst_node.child.pop(-1)
                ast_node.child.append(VarDeclarator.transform(cst_node, ast_node))
            else:
                ast_node = cls("function decl", father_node)
                ast_node.child.append(cls(cst_node.child[0].symbol, ast_node))
                if len(cst_node.child) > 3:
                    cst_node.child.pop(0)
                    cst_node.child.pop(0)
                    cst_node.child.pop(-1)
                    ast_node.child.append(ParamList.transform(cst_node.child[0], ast_node))
            
            return ast_node
                
        else:
            return cls(cst_node.child[0].symbol, father_node)


class FunctionDefinition(AbstractSyntaxTreeNode):

    @classmethod
    def transform(cls, type_spec, cst_node, father_node):
        ast_node = cls("function definition", father_node)

        ast_node.child.append(type_spec)
        ast_node.child.append(VarDeclarator.transform(cst_node.child[0], ast_node))
        ast_node.child.append(CompoundStat.transform(cst_node.child[1], ast_node))

        return ast_node


class ParamList(AbstractSyntaxTreeNode):

    @classmethod
    def transform(cls, cst_node, father_node):
        ast_node = cls("param list", father_node)
        
        for node in cst_node.child:
            if node.symbol == "param decl":
                ast_node.child.append(ParamDecl.transform(node, ast_node))

        return ast_node


class ParamDecl(AbstractSyntaxTreeNode):

    @classmethod
    def transform(cls, cst_node, father_node):
        ast_node = cls("param decl", father_node)

        for node in cst_node.child:
            ast_node.child.append(VarDeclarator.transform(node, ast_node))

        return ast_node


class CompoundStat(AbstractSyntaxTreeNode):

    @classmethod
    def transform(cls, cst_node, father_node):
        ast_node = cls("compound statement", father_node)

        for node in cst_node.child:
            if node.symbol == "declaration list":
                ast_node.child.append(LocalDeclList.transform(node, ast_node))
            elif node.symbol == "statement list":
                ast_node.child.append(StatList.transform(node, ast_node))

        return ast_node


class LocalDeclList(AbstractSyntaxTreeNode):

    @classmethod
    def transform(cls, cst_node, father_node):
        ast_node = cls("declaration list", father_node)

        for node in cst_node.child:
            ast_node.child.append(InitDeclaratorList.transform(node.child[0], node.child[1], ast_node))

        return ast_node


class StatList(AbstractSyntaxTreeNode):

    @classmethod
    def transform(cls, cst_node, father_node):
        ast_node = cls("statement list", father_node)

        for node in cst_node.child:
            ast_node.child.append(Statement.transform(node, ast_node))

        return ast_node


class Statement(AbstractSyntaxTreeNode):

    @classmethod
    def transform(cls, cst_node, father_node):
        if cst_node.child[0].symbol == "labeled statement":
            return LabeledStat.transform(cst_node.child[0], father_node)
        elif cst_node.child[0].symbol == "expression statement":
            return ExpStat.transform(cst_node.child[0], father_node)
        elif cst_node.child[0].symbol == "compound statement":
            return CompoundStat.transform(cst_node.child[0], father_node)
        elif cst_node.child[0].symbol == "selection statement":
            return SelectionStat.transform(cst_node.child[0], father_node)
        elif cst_node.child[0].symbol == "iteration statement":
            return IterationStat.transform(cst_node.child[0], father_node)
        elif cst_node.child[0].symbol == "jump statement":
            return JumpStat.transform(cst_node.child[0], father_node)


class LabeledStat(AbstractSyntaxTreeNode):

    @classmethod
    def transform(cls, cst_node, father_node):
        ast_node = None

        if isinstance(cst_node.child[0].symbol, Token) and cst_node.child[0].symbol.value == "case":
            ast_node = cls(cst_node.child[0].symbol, father_node)
            ast_node.child.append(Expression.transform(cst_node.child[1], ast_node))
            ast_node.child.append(Statement.transform(cst_node.child[1], ast_node))
        elif isinstance(cst_node.child[0].symbol, Token) and cst_node.child[0].symbol.value == "default":
            ast_node = cls(cst_node.child[0].symbol, father_node)
            ast_node.child.append(Statement.transform(cst_node.child[1], ast_node))

        return ast_node


class ExpStat(AbstractSyntaxTreeNode):

    @classmethod
    def transform(cls, cst_node, father_node):
        ast_node = cls("expression statement", father_node)

        if cst_node.child[0].symbol == "expression":
            ast_node.child.append(Expression.transform(cst_node.child[0], ast_node))

        return ast_node


class SelectionStat(AbstractSyntaxTreeNode):

    @classmethod
    def transform(cls, cst_node, father_node):
        ast_node = None

        if isinstance(cst_node.child[0].symbol, Token) and cst_node.child[0].symbol.value == "if":
            ast_node = cls("if then else", father_node)
            for node in cst_node.child[1:]:
                if node.symbol == "expression":
                    ast_node.child.append(Expression.transform(node, ast_node))
                elif node.symbol == "statement":
                    ast_node.child.append(Statement.transform(node, ast_node))
                elif isinstance(node.symbol, Token) and node.symbol.value == "else":
                    ast_node.child.append(Statement.transform(node, ast_node))
        else:
            ast_node = cls("switch", father_node)
            for node in cst_node[1:]:
                if node.symbol == "expression":
                    ast_node.child.append(Expression.transform(node, ast_node))
                elif node.symbol == "statement":
                    ast_node.child.append(Statement.transform(node, ast_node))

        return ast_node


class IterationStat(AbstractSyntaxTreeNode):

    @classmethod
    def transform(cls, cst_node, father_node):
        ast_node = None

        if isinstance(cst_node.child[0].symbol, Token) and cst_node.child[0].symbol.value == "do":
            ast_node = cls("do while", father_node)
        else:
            ast_node = cls("while do", father_node)
        for node in cst_node.child[1:]:
            if node.symbol == "expression":
                ast_node.child.append(Expression.transform(node, ast_node))
            elif node.symbol == "statement":
                ast_node.child.append(Statement.transform(node, ast_node))

        return ast_node


class JumpStat(AbstractSyntaxTreeNode):

    # TODO: Do I need check if there are semantic error.
    @classmethod
    def transform(cls, cst_node, father_node):
        ast_node = cls(cst_node.child[0].symbol, father_node)
        if isinstance(cst_node.child[1].symbol, str) and cst_node.child[1].symbol == "expression":
            ast_node.child.append(Expression.transform(cst_node.child[1], ast_node))

        return ast_node


class Expression(AbstractSyntaxTreeNode):

    @classmethod
    def transform(cls, cst_node, father_node):
        ast_node = None

        if len(cst_node.child) > 1:
            ast_node = cls(cst_node.child.pop(1).symbol, father_node)
            ast_node.child.append(AsignmentExp.transform(cst_node.child.pop(0), ast_node))
            ast_node.child.append(Expression.transform(cst_node, ast_node))
        else:
            return AsignmentExp.transform(cst_node.child[0], father_node)

        return ast_node


class AsignmentExp(AbstractSyntaxTreeNode):

    @classmethod
    def transform(cls, cst_node, father_node):
        ast_node = None

        if len(cst_node.child) > 1:
            if cst_node.child[1].symbol.value == '=':
                ast_node = cls(cst_node.child.pop(1).symbol,father_node)
                ast_node.child.append(UnaryExp.transform(cst_node.child.pop(0), ast_node))
                ast_node.child.append(cls.transform(cst_node, ast_node))
            else:
                ast_node = cls('=', father_node)
                ast_node.child.append(UnaryExp.transform(cst_node.child[0], ast_node))
                ast_node.child.append(cst_node.child.pop(1).symbol.value[0])
                ast_node.child[1].child.append(UnaryExp.transform(cst_node.child.pop(0), ast_node))
                ast_node.child[1].child.append(cls.transform(cst_node, ast_node))
        else:
            return LogicalOrExp.transform(cst_node.child[0], father_node)

        return ast_node


class LogicalOrExp(AbstractSyntaxTreeNode):

    @classmethod
    def transform(cls, cst_node, father_node):
        ast_node = None

        if len(cst_node.child) > 1:
            ast_node = cls(cst_node.child.pop(1).symbol, father_node)
            ast_node.child.append(LogicalAndExp.transform(cst_node.child.pop(0), ast_node))
            ast_node.child.append(LogicalOrExp.transform(cst_node, ast_node))
        else:
            return LogicalAndExp.transform(cst_node.child[0], father_node)

        return ast_node


class LogicalAndExp(AbstractSyntaxTreeNode):

    @classmethod
    def transform(cls, cst_node, father_node):
        ast_node = None

        if len(cst_node.child) > 1:
            ast_node = cls(cst_node.child.pop(1).symbol, father_node)
            ast_node.child.append(EqualityExp.transform(cst_node.child.pop(0), ast_node))
            ast_node.child.append(LogicalAndExp.transform(cst_node, ast_node))
        else:
            return EqualityExp.transform(cst_node.child[0], father_node)

        return ast_node


class EqualityExp(AbstractSyntaxTreeNode):

    @classmethod
    def transform(cls, cst_node, father_node):
        ast_node = None

        if len(cst_node.child) > 1:
            ast_node = cls(cst_node.child.pop(1).symbol, father_node)
            ast_node.child.append(RelationalExp.transform(cst_node.child.pop(0), ast_node))
            ast_node.child.append(EqualityExp.transform(cst_node, ast_node))
        else:
            return RelationalExp.transform(cst_node.child[0], father_node)

        return ast_node


class RelationalExp(AbstractSyntaxTreeNode):

    @classmethod
    def transform(cls, cst_node, father_node):
        ast_node = None

        if len(cst_node.child) > 1:
            ast_node = cls(cst_node.child.pop(1).symbol, father_node)
            ast_node.child.append(AdditiveExp.transform(cst_node.child.pop(0), ast_node))
            ast_node.child.append(RelationalExp.transform(cst_node, ast_node))
        else:
            return AdditiveExp.transform(cst_node.child[0], father_node)

        return ast_node


class AdditiveExp(AbstractSyntaxTreeNode):

    @classmethod
    def transform(cls, cst_node, father_node):
        ast_node = None

        if len(cst_node.child) > 1:
            ast_node = cls(cst_node.child.pop(1).symbol, father_node)
            ast_node.child.append(MultExp.transform(cst_node.child.pop(0), ast_node))
            ast_node.child.append(AdditiveExp.transform(cst_node, ast_node))
        else:
            return MultExp.transform(cst_node.child[0], father_node)

        return ast_node


class MultExp(AbstractSyntaxTreeNode):

    @classmethod
    def transform(cls, cst_node, father_node):
        ast_node = None

        if len(cst_node.child) > 1:
            ast_node = cls(cst_node.child.pop(1).symbol, father_node)
            ast_node.child.append(CastExp.transform(cst_node.child.pop(0), ast_node))
            ast_node.child.append(MultExp.transform(cst_node, ast_node))
        else:
            return CastExp.transform(cst_node.child[0], father_node)

        return ast_node


class CastExp(AbstractSyntaxTreeNode):

    @classmethod
    def transform(cls, cst_node, father_node):
        ast_node = None

        if isinstance(cst_node.child[0].symbol, Token) and cst_node.child[0].symbol.value == '(':
            ast_node = cls(cst_node.child.pop(1).symbol, father_node)
            cst_node.child.pop(0)
            cst_node.child.pop(0)
            ast_node.child.append(UnaryExp.transform(cst_node, ast_node))
        else:
            return UnaryExp.transform(cst_node.child[0], father_node)


class UnaryExp(AbstractSyntaxTreeNode):

    @classmethod
    def transform(cls, cst_node, father_node):
        ast_node = None

        if isinstance(cst_node.child[0].symbol, Token) and cst_node.child[0].symbol.value in ('++', '--'):
            cst_node.child[0].symbol.value += "_pre"
            ast_node = cls(cst_node.child[0].symbol, father_node)
            if cst_node.child[1].symbol.value in ('+', '-', '!'):
                raise TransformException("semantic error")
            else:
                ast_node.child.append(PostfixExp.transform(cst_node.child[1], ast_node))
        else:
            if isinstance(cst_node.child[0].symbol, Token) and cst_node.child[0].symbol.value in ('+', '-', '!'):
                ast_node = cls(cst_node.child[0].symbol, father_node)
                ast_node.child.append(CastExp.transform(cst_node.child[0], ast_node))
            else:
                return PostfixExp.transform(cst_node.child[0], father_node)

        return ast_node


class PostfixExp(AbstractSyntaxTreeNode):

    @classmethod
    def transform(cls, cst_node, father_node):

        if len(cst_node.child) > 1:
            ast_node = None
            if isinstance(cst_node.child[1].symbol, Token) and cst_node.child[1].symbol.value in ('++', '--'):
                cst_node.child[1].symbol.value += "_post"
                ast_node = cls(cst_node.child[1].symbol, father_node)
                ast_node.child.append(PrimaryExp.transform(cst_node.child[0], ast_node))
            elif isinstance(cst_node.child[1].symbol, Token) and cst_node.child[1].symbol.value == "(":
                ast_node = cls("call", father_node)
                ast_node.child.append(PrimaryExp.transform(cst_node.child[0], ast_node))
                if isinstance(cst_node.child[2].symbol, str) and cst_node.child[2].symbol == "argument expression":
                    ast_node.child.append(ArgumentExpList.transform(cst_node.child[2], ast_node))
            else:
                ast_node = cls("array deref", father_node)
                cst_node.child.pop(-1)
                ast_node.child.append(Expression.transform(cst_node.child.pop(-1), ast_node))
                cst_node.child.pop(-1)
                ast_node.child.append(PostfixExp.transform(cst_node, ast_node))
            return ast_node

        else:
            return PrimaryExp.transform(cst_node.child[0], father_node)


class PrimaryExp(AbstractSyntaxTreeNode):

    @classmethod
    def transform(cls, cst_node, father_node):
        if isinstance(cst_node.symbol, str) and cst_node.symbol == "bracket expression":
            return Expression.transform(cst_node.child[1], father_node)
        else:
            return cls(cst_node.symbol, father_node)

class ArgumentExpList(AbstractSyntaxTreeNode):

    @classmethod
    def transform(cls, cst_node, father_node):
        ast_node = cls("argument expression", father_node)

        for node in cst_node.child:
            if not isinstance(cst_node.symbol, Token):
                ast_node.child.append(AsignmentExp.transform(node, ast_node))

        return ast_node
