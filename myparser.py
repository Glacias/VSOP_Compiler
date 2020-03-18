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
    # Precedence and associativity rules
    precedence = (
    ('nonassoc', 'if_then', 'let_prec'),
    ('nonassoc', 'else', 'while_prec', 'let_prec_assign'),
    ('right', 'assign'),
    ('left', 'and'),
    ('right', 'not'),
    ('nonassoc', 'lower', 'lower_equal', 'equal'),
    ('left', 'plus', 'minus'),
    ('left', 'times', 'div'),
    ('right', 'uminus', 'isnull'),
    ('right', 'pow'),
    ('left', 'dot'),
    )

    # Init
    def __init__(self, lexer, file):
        self.lex = lexer
        self.tokens = lexer.tokens
        self.keyword = lexer.keyword
        self.operator = lexer.operator
        self.ast_root = Program()
        global file_name
        file_name = file

    # Build the parser
    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)

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
                      | Class_body Field
                      | Class_body Method'''
        if(len(p)==1):
            p[0] = Class()
        else:
            if(isinstance(p[2], Field)):
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

    ## Expressions
    def p_Expr_If_then(self, p):
        '''Expr : if Expr then Expr %prec if_then
                | if Expr then Expr else Expr'''
        if(len(p)==7):
            p[0] = Expr_if(p[2], p[4])
            p[0].add_else_expr(p[6])
        else:
            p[0] = Expr_if(p[2], p[4])

    def p_Expr_while(self, p):
        'Expr : while Expr do Expr %prec while_prec'
        p[0] = Expr_while(p[2], p[4])

    def p_Expr_let(self, p):
        '''Expr : let object_identifier colon Type in Expr %prec let_prec
                | let object_identifier colon Type assign Expr in Expr %prec let_prec_assign'''
        if(len(p)==7):
            p[0] = Expr_let(p[2], p[4], p[6])
        else:
            p[0] = Expr_let(p[2], p[4], p[8])
            p[0].add_init_expr(p[6])

    def p_Expr_assign(self, p):
        'Expr : object_identifier assign Expr'
        p[0] = Expr_assign(p[1], p[3])

    def p_Expr_uminus(self, p):
        'Expr : minus Expr %prec uminus'
        p[0] = Expr_UnOp(p[1], p[2])

    def p_Expr_UnOp(self, p):
        '''Expr : not Expr
                | isnull Expr'''
        p[0] = Expr_UnOp(p[1], p[2])

    def p_Expr_BinOp(self, p):
        '''Expr : Expr and Expr
                | Expr equal Expr
                | Expr lower Expr
                | Expr lower_equal Expr
                | Expr plus Expr
                | Expr minus Expr
                | Expr times Expr
                | Expr div Expr
                | Expr pow Expr'''
        p[0] = Expr_BinOp(p[2], p[1], p[3])

    def p_Expr_Call(self, p):
        '''Expr : object_identifier lpar Args rpar
                | Expr dot object_identifier lpar Args rpar'''
        if(len(p)==5):
            p[0] = Expr_Call(p[1], p[3])
        else:
            p[0] = Expr_Call(p[3], p[5])
            p[0].add_object_expr(p[1])

    def p_Expr_New(self, p):
        'Expr : new type_identifier'
        p[0] = Expr_New(p[2])

    def p_Expr_Object_id(self, p):
        'Expr : object_identifier'
        p[0] = Expr_Object_identifier(p[1])

    def p_Expr_literal(self, p):
        'Expr : Literal'
        p[0] = p[1]

    def p_Expr_Unit(self, p):
        'Expr : lpar rpar'
        p[0] = Expr_Unit()

    def p_Expr_Par_expr(self, p):
        'Expr : lpar Expr rpar'
        p[0] = p[2]

    def p_Expr_block(self,p):
        'Expr : Block'
        p[0] = p[1]

    def p_Args(self, p):
        '''Args :
                | Expr
                | Args comma Expr'''
        if(len(p)==1):
            p[0] = Args()
        elif(len(p)==2):
            p[0] = Args()
            p[0].add_arg(p[1])
        else:
            p[0] = p[1]
            p[0].add_arg(p[3])

    # Literal
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

    #def p_Test(self, p):
    #    '''Test : integer_literal
    #            | Test integer_literal'''
    #    if(len(p)==2):
    #        p.test = Test([p[1]])
    #    else:
    #        p.test.add_class(p[2])
    #    p[0] = p.test

    def p_error(self, p):
        if not p:
            error_str = file_name + ":" + str(self.lex.lexer.lineno)
            error_str += ":" + str(self.lex.lexer.lexpos - self.lex.lexer.line_end_pos-1)
            error_str += ": syntax error.\n  "
            error_str += "The parser reached the end of file and detected an error, this is probably due to a missing brace\n"
            sys.stderr.write(error_str)
        else:
            error_message(p, "An error occured while parsing the following token : " + str(p.value))
        sys.exit(1)




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
        str = "Class(" + self.name + ", " + self.parent + ", "
        str += get_list_string(self.fields) + ", "
        str += get_list_string(self.methods)
        str += ")"
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
        if(self.init_expr==""):
            str = get_obejct_string("Field", [self.name, self.type])
        else:
            str = get_obejct_string("Field", [self.name, self.type, self.init_expr])
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
        str = get_obejct_string("Method", [self.name, self.formals, self.ret_type, self.block])
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
        str = get_list_string(self.list_formals)
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
        if(len(self.list_expr)==1):
            str = self.list_expr[0].__str__()
        else:
            str = get_list_string(self.list_expr)
        return str

    def add_expr(self, expr):
        self.list_expr.append(expr)

## Expressions
class Expr(Node):
    pass

class Expr_if(Expr):
    def __init__(self, cond_expr, then_expr):
        self.cond_expr = cond_expr
        self.then_expr = then_expr
        self.else_expr = ""

    def __str__(self):
        if(self.else_expr==""):
            str = get_obejct_string("If", [self.cond_expr, self.then_expr])
        else:
            str = get_obejct_string("If", [self.cond_expr, self.then_expr, self.else_expr])
        return str

    def add_else_expr(self, expr):
        self.else_expr = expr

class Expr_while(Expr):
    def __init__(self, cond_expr, body_expr):
        self.cond_expr = cond_expr
        self.body_expr = body_expr

    def __str__(self):
        return get_obejct_string("While", [self.cond_expr, self.body_expr])

class Expr_let(Expr):
    def __init__(self, name, type, scope_expr):
        self.name = name
        self.type = type
        self.init_expr = ""
        self.scope_expr = scope_expr

    def __str__(self):
        if(self.init_expr==""):
            str = get_obejct_string("Let", [self.name, self.type, self.scope_expr])
        else:
            str = get_obejct_string("Let", [self.name, self.type, self.init_expr, self.scope_expr])
        return str

    # Add init expr
    def add_init_expr(self, init_expr):
        self.init_expr = init_expr

class Expr_assign(Expr):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr
    def __str__(self):
        return get_obejct_string("Assign", [self.name, self.expr])

class Expr_UnOp(Expr):
    def __init__(self, unop, expr):
        self.unop = unop
        self.expr = expr
    def __str__(self):
        return get_obejct_string("UnOp", [self.unop, self.expr])

class Expr_BinOp(Expr):
    def __init__(self, op, left_expr, right_expr):
        self.op = op
        self.left_expr = left_expr
        self.right_expr = right_expr
    def __str__(self):
        return get_obejct_string("BinOp", [self.op, self.left_expr, self.right_expr])

class Expr_Call(Expr):
    def __init__(self, method_name, expr_list):
        self.object_expr = "self"
        self.method_name = method_name
        self.expr_list = expr_list
    def __str__(self):
        return get_obejct_string("Call", [self.object_expr, self.method_name, self.expr_list])
    def add_object_expr(self, expr):
        self.object_expr = expr

class Expr_Object_identifier(Expr):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name.__str__()

class Expr_New(Expr):
    def __init__(self, type_name):
        self.type_name = type_name
    def __str__(self):
        return get_obejct_string("New", [self.type_name])

class Expr_Unit(Expr):
    def __init__(self):
        self.unit = "()"
    def __str__(self):
        return self.unit.__str__()

class Args(Node):
    def __init__(self):
        self.list_args = []
    def __str__(self):
        return get_list_string(self.list_args)
    def add_arg(self, arg):
        self.list_args.append(arg)

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
        str += el.__str__() + ', '
    str = str[:-2]
    str += ']'
    return str

# Generate the string of an object (Ex : If(1, 2))
def get_obejct_string(name, list):
    str = name + "("
    if(len(list)==0):
        return str + ")"
    for el in list:
        str += el.__str__() + ", "
    str = str[:-2] + ")"
    return str

# Generate error message
def error_message(token, description):
    error_str = file_name + ":" + str(token.lexer.lineno)
    error_str += ":" + str(token.lexpos - token.lexer.line_end_pos)
    error_str += ": syntax error.\n  " + description + "\n"
    sys.stderr.write(error_str)
