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
