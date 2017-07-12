"""
transform a concrete syntax tree(CST) to a abstract syntax tree(AST)

[AST structure form](http://www.cs.xu.edu/csci310/09s/ast.html)
"""
from .parser import ParseNode
from .exceptions import TransformException


class SourceRoot(ParseNode):

    @classmethod
    def transform(cls, cst_node):
        ast_node = cls("source root")

        if cst_node.symbol == "translation Unit":
            for node in cst_node.child:
                ast_node.child.append(ExternalDecl.transform(node))
        else:
            raise TransformException("expect a translation Unit node as the root of AST.")

        return cst_node


class ExternalDecl(ParseNode):

    @classmethod
    def transform(cls, cst_node):
        ast_node = cls("external declaration")

        ast_node.child.append(cst_node.child[0])
        if cst_node.child[1].symbol == "init declarator list":
            ast_node.child.append(InitDeclaratorList.transform(cst_node[1]))
        else:
            ast_node.child.append(FunctionDefinition.transform(cst_node[1]))

        return cst_node


class InitDeclaratorList(ParseNode):

    @classmethod
    def transform(cls, cst_node):
        ast_node = cls("init declarator list")

        for node in cst_node.child:
            if len(node.child) != 1:
                ast_node.child.append(Annasign.transform(node))
            else:
                ast_node.child.append(node.child[0])

        return ast_node


class FunctionDefinition(ParseNode):

    @classmethod
    def transform(cls, cst_node):
        ast_node = cls("function definition")

        ast_node.child.append(cst_node.child[0])
        for node in ast_node.child[1:]:
            if node.symbol == "param list":
                ast_node.child.append(ParamList.transform(node))
            elif node.symbol == "compound statement":
                ast_node.child.append(CompoundStat.transform(node))

        return ast_node


class ParamList(ParseNode):

    @classmethod
    def transform(cls, cst_node):
        ast_node = cls("param list")
        
        for node in ast_node.child:
            if node.symbol == "param decl":
                ast_node.child.append(ParamDecl.transform(node))

        return ast_node


class ParamDecl(ParseNode):

    @classmethod
    def transform(cls, cst_node):
        ast_node = cls("param decl")

        for node in cst_node.child:
            ast_node.child.append(node)

        return ast_node


# TODO: finish this module.
