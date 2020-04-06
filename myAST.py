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
            str = get_object_string("Field", [self.name, self.type])
        else:
            str = get_object_string("Field", [self.name, self.type, self.init_expr])
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
        str = get_object_string("Method", [self.name, self.formals, self.ret_type, self.block])
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
            str = get_object_string("If", [self.cond_expr, self.then_expr])
        else:
            str = get_object_string("If", [self.cond_expr, self.then_expr, self.else_expr])
        return str

    def add_else_expr(self, expr):
        self.else_expr = expr

class Expr_while(Expr):
    def __init__(self, cond_expr, body_expr):
        self.cond_expr = cond_expr
        self.body_expr = body_expr

    def __str__(self):
        return get_object_string("While", [self.cond_expr, self.body_expr])

class Expr_let(Expr):
    def __init__(self, name, type, scope_expr):
        self.name = name
        self.type = type
        self.init_expr = ""
        self.scope_expr = scope_expr

    def __str__(self):
        if(self.init_expr==""):
            str = get_object_string("Let", [self.name, self.type, self.scope_expr])
        else:
            str = get_object_string("Let", [self.name, self.type, self.init_expr, self.scope_expr])
        return str

    # Add init expr
    def add_init_expr(self, init_expr):
        self.init_expr = init_expr

class Expr_assign(Expr):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr
    def __str__(self):
        return get_object_string("Assign", [self.name, self.expr])

class Expr_UnOp(Expr):
    def __init__(self, unop, expr):
        self.unop = unop
        self.expr = expr
    def __str__(self):
        return get_object_string("UnOp", [self.unop, self.expr])

class Expr_BinOp(Expr):
    def __init__(self, op, left_expr, right_expr):
        self.op = op
        self.left_expr = left_expr
        self.right_expr = right_expr
    def __str__(self):
        return get_object_string("BinOp", [self.op, self.left_expr, self.right_expr])

class Expr_Call(Expr):
    def __init__(self, method_name, expr_list):
        self.object_expr = "self"
        self.method_name = method_name
        self.expr_list = expr_list
    def __str__(self):
        return get_object_string("Call", [self.object_expr, self.method_name, self.expr_list])
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
        return get_object_string("New", [self.type_name])

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
def get_object_string(name, list):
    str = name + "("
    if(len(list)==0):
        return str + ")"
    for el in list:
        str += el.__str__() + ", "
    str = str[:-2] + ")"
    return str