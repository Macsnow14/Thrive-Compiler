# Thrive-Compiler

[![Build Status](https://travis-ci.org/Thrimbda/Thrive-Compiler.svg?branch=master)](https://travis-ci.org/Thrimbda/Thrive-Compiler)

compiler for Thrilang.

## what is Thrilang?

Basically thrilang a subset of C programming language.

want to know more? see the features list below.

### FEATURE

#### Var types

- int 
- float
- bool
- char

#### Value

#### Expressions

##### Arithmetic expression

`+`, `-`, `*`, `/`, `++`, `--`

##### Relational expression

`<`, `>`, `<=`, `>=`, `==`, `!=`

##### Boolean expression

`!`, `&&`, `||`

#### Statement

- Assignment
- Conditional
- Loop
- Procedure Call
- Define

## TODO

### basic

- [x] Lexer for lexical analysis.

- [x] Parser for syntactic analysis and generate concrete syntax tree.

- [ ] transfrom concrete syntax tree to abstract syntax tree.

- [ ] generate quad from AST.

### enhancement

- [x] Add travis CI uni test.

- [ ] visualize.
    - [x] concrete syntax tree.

    - [ ] abstract syntax tree.
