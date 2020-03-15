# -----------------------------------------------------------------------------
# parser.py
#
# File responsible for the syntax analysis
# Made by Simon Bernard and Ivan Klapka for the Project 1 : lexical analysis
# University of Liège - Academic year 2019-2020 - INFO0085-1 Compilers course
# -----------------------------------------------------------------------------

import ply.yacc as yacc
import sys

class MyParser(object):
    def __init__(self, lexer):
        self.tokens = lexer.tokens
        self.keyword = lexer.keyword
        self.operator = lexer.operator
        self.ast_root = Program()

    ### Rules for parsing
    def p_Program(self, p):
        '''Program : Class
                   | Program Class'''
        if(len(p)==2):
            self.ast_root.add_class(p[1])
        else:
            self.ast_root.add_class(p[2])
        p[0] = self.ast_root

    def p_Class_body(self, p):
        # To change
        '''Class_body :
                      | Class_body Test
                      | Class_body object_identifier'''
        if(len(p)==1):
            p[0] = Class()
        else:
            if(isinstance(p[2],Test)):
                p[1].add_field(p[2])
            else:
                p[1].add_method(p[2])
            p[0] = p[1]

    def p_Class(self, p):
        '''Class : class type_identifier lbrace Class_body rbrace
                 | class type_identifier extends type_identifier lbrace Class_body rbrace'''
        if(len(p)==6):
            p[0] = p[4]
            p[0].change_name(p[2])
        else:
            p[0] = p[6]
            p[0].change_name(p[2])
            p[0].change_parent(p[4])

    def p_Field(self, p):
        '''Field : object_identifier colon Type semicolon
                 | object_identifier colon Type assign Expr semicolon'''
        if(len(p)==5):
            p[0] = Field(p[1], p[3])
        else:
            p[0] = Field(p[1], p[3])
            p[0].add_init_expr(p[5])

    def p_Method(self, p):
        'Method : object_identifier lpar Formals rpar colon Type Block'
        p[0] = Method(p[1], p[3], p[6], p[7])

    def p_Type(self, p):
        '''Type : type_identifier
                | int32
                | bool
                | string
                | unit'''
        p[0] = Type(p[1])

    def p_Formals(self, p):
        '''Formals :
                   | Formal
                   | Formals comma Formal'''
        if(len(p)==1):
            p[0] = Formals()
        elif(len(p)==2):
            p[0] = Formals()
            p[0].add_formal(p[1])
        else:
            p[0] = p[1]
            p[0].add_formal(p[3])

    def p_Formal(self, p):
        'Formal : object_identifier colon Type'
        p[0] = Formal(p[1], p[3])

    def p_Block(self, p):
        'Block : lbrace Block_body rbrace'
        p[0] = p[2]

    def p_Block_body(self, p):
        '''Block_body : Expr
                      | Block_body semicolon Expr'''
        if(len(p)==2):
            p[0] = Block()
            p[0].add_expr(p[1])
        else:
            p[0] = p[1]
            p[0].add_expr(p[3])

    # TO CHANGE
    def p_Expr(self, p):
        '''Expr : Literal'''
        p[0] = p[1]

    def p_Literal(self, p):
        '''Literal : integer_literal
                   | string_literal
                   | Boolean_literal'''
        p[0] = Literal(p[1])

    def p_Boolean_literal(self, p):
        '''Boolean_literal : true
                           | false'''
        if(p[1]=="true"):
            p[0] = Boolean_literal(True)
        else:
            p[0] = Boolean_literal(False)

    def p_Test(self, p):
        '''Test : integer_literal
                | Test integer_literal'''
        if(len(p)==2):
            p.test = Test([p[1]])
        else:
            p.test.add_class(p[2])
        p[0] = p.test

    def p_error(self, t):
        print("Syntax error at '%s'" % t.value)

    # Build the parser
    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)

##### Classes for AST
# General class node
class Node:
    pass

# Program
class Program(Node):
    def __init__(self):
        self.list_class = []

    # Print the list of class
    def __str__(self):
        return get_list_string(self.list_class)

    # Add a class to the program
    def add_class(self, c):
        self.list_class.append(c)

# Class
class Class(Node):
    def __init__(self):
        self.name = ""
        self.parent = "Object"
        self.fields = []
        self.methods = []

    # Print the class
    def __str__(self):
        str = "Class(" + self.name + ", " + self.parent + ", \n\t"
        str += get_list_string(self.fields) + ", \n\t"
        str += get_list_string(self.methods)
        str += ")\n"
        return str

    # Name the class
    def change_name(self, name):
        self.name = name

    # Parent of the class (default = Object)
    def change_parent(self, parent):
        self.parent = parent

    # Add a field
    def add_field(self, field):
        self.fields.append(field)

    # Add a method
    def add_method(self, method):
        self.methods.append(method)

# Field
class Field(Node):
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.init_expr = ""

    def __str__(self):
        str = "Field(" + self.name + ", " + self.type.__str__()
        if(self.init_expr != ""):
            str += ", " + self.init_expr.__str__()
        str += ")"
        return str

    # Add init expr
    def add_init_expr(self, init_expr):
        self.init_expr = init_expr

class Method(Node):
    def __init__(self, name, formals, ret_type, block):
        self.name = name
        self.formals = formals
        self.ret_type = ret_type
        self.block = block

    def __str__(self):
        str = "Method(" + self.name + ", " + self.formals.__str__()
        str += ", " + self.ret_type.__str__()
        str += ", " + self.block.__str__() + ')'
        return str

class Type(Node):
    def __init__(self, type):
        self.type = type

    def __str__(self):
        return self.type.__str__()

class Formals(Node):
    def __init__(self):
        self.list_formals = []

    def __str__(self):
        str = get_list_string(formals)
        return str

    def add_formal(self, formal):
        self.list_formals.append(formal)

class Formal(Node):
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __str__(self):
        str = self.name + " : " + self.type.__str__()
        return str

class Block(Node):
    def __init__(self):
        self.list_expr = []

    def __str__(self):
        if(len(self.list_exp)==1):
            str = self.list_exp[0].__str__()
        else:
            str = get_list_string(self.list_exp)
        return str

    def add_expr(self, expr):
        self.list_expr.append(expr)

class Literal(Node):
    def __init__(self, literal):
        self.literal = literal

    def __str__(self):
        str = self.literal.__str__()
        return str

class Boolean_literal(Node):
    def __init__(self, bool):
        self.bool = bool

    def __str__(self):
        if(self.bool):
            str = "true"
        else:
            str = "false"
        return str

class Test(Node):
    def __init__(self, list):
        self.list = list

    def add_class(self, c):
        self.list.append(c)
    def __str__(self):
        return get_list_string(self.list)

### General Functions
# Generate the string of a list
def get_list_string(list):
    if(len(list)==0):
        return "[]"
    str = '['
    for el in list:
        str += el.__str__() + ','
    str = str[:-1]
    str += ']'
    return str
