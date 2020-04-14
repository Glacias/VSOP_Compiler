##### Classes for AST
# General class node
class Node:
    def __init__(self):
        self.typeChecked = ""
        self.line = -1
        self.col = -1

    def add_position(self, line, col):
        self.line = line
        self.col = col

    def add_position_from_node(self, cl):
        self.line = cl.line
        self.col = cl.col

# Program
class Program(Node):
    def __init__(self):
        Node.__init__(self)
        self.list_class = []

    # Print the list of class
    def __str__(self):
        return get_list_string(self.list_class)

    # Add a class to the program
    def add_class(self, c):
        self.list_class.append(c)

    # Check the type of expression in the tree
    def checkTypeTree(self, gst, file_name, error_buffer):
        # For every class
        for cl in self.list_class:
            # Check type tree
            cl.checkTypeTree(gst, file_name, error_buffer)

# Class
class Class(Node):
    def __init__(self):
        Node.__init__(self)
        self.name = ""
        self.nameLine = -1
        self.nameCol = -1
        self.parent = "Object"
        self.parentLine = -1
        self.parentCol = -1
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

    # Add position for name
    def add_position_name(self, line, col):
        self.nameLine = line
        self.nameCol = col

    # Add position for parent
    def add_position_parent(self, line, col):
        self.parentLine = line
        self.parentCol = col

    # Check the type of expression in the tree
    def checkTypeTree(self, gst, file_name, error_buffer):
        # For every field
        for fl in self.fields:
            fl.checkTypeTree(gst, file_name, error_buffer)
        # For every method
        for mt in self.methods:
            mt.checkTypeTree(gst, file_name, error_buffer)

# Field
class Field(Node):
    def __init__(self, name, type):
        Node.__init__(self)
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

    # Check the type of expression in the tree
    def checkTypeTree(self, gst, file_name, error_buffer):
        if self.init_expr != "":
            # Create a symbol table
            st = symbolTable()
            # Check the expression
            typeExpr = self.init_expr.checkExpr(gst, st, file_name, error_buffer)
            # Check that the initializer type corresponds to the field type
            if not gst.areConform(typeExpr, self.type.type):
                error_message_ast(self.type.line, self.type.col, "the type of the initializer (" + typeExpr + ") must conform to the declared type of the field (" + self.type.type + ")", file_name, error_buffer)

class Method(Node):
    def __init__(self, name, formals, type, block):
        Node.__init__(self)
        self.name = name
        self.formals = formals
        self.type = type
        self.block = block

    def __str__(self):
        str = get_object_string("Method", [self.name, self.formals, self.type, self.block])
        return str

    # Check the type of expression in the tree
    def checkTypeTree(self, gst, file_name, error_buffer):
        pass

class Type(Node):
    def __init__(self, type):
        Node.__init__(self)
        self.type = type

    def __str__(self):
        return self.type.__str__()

class Formals(Node):
    def __init__(self):
        Node.__init__(self)
        self.list_formals = []

    def __str__(self):
        str = get_list_string(self.list_formals)
        return str

    def add_formal(self, formal):
        self.list_formals.append(formal)

class Formal(Node):
    def __init__(self, name, type):
        Node.__init__(self)
        self.name = name
        self.type = type

    def __str__(self):
        str = self.name + " : " + self.type.__str__()
        return str

class Block(Node):
    def __init__(self):
        Node.__init__(self)
        self.list_expr = []

    def __str__(self):
        if(len(self.list_expr)==1):
            str = self.list_expr[0].__str__()
        else:
            str = get_list_string(self.list_expr)
        return str

    def add_expr(self, expr):
        self.list_expr.append(expr)

    # Check the expressions of the block
    def checkExpr(self, gst, st, file_name, error_buffer):
        # Open a new context
        st.enter_ctx()
        # Check all expression
        for exp in self.list_expr:
            typeExpr = exp.checkExpr(gst, st, file_name, error_buffer)
        # The type of the last expression is the expression of the block
        self.typeChecked = typeExpr
        # Exit the context
        st.exit_ctx()
        return self.typeChecked

## Expressions
class Expr(Node):
    pass

class Expr_if(Expr):
    def __init__(self, cond_expr, then_expr):
        Node.__init__(self)
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

    # Check the expressions of the conditional
    def checkExpr(self, gst, st, file_name, error_buffer):
        # Check expr of if and then
        typeCondExpr = self.cond_expr.checkExpr(gst, st, file_name, error_buffer)
        typeThenExpr = self.then_expr.checkExpr(gst, st, file_name, error_buffer)
        # Cond expr must be of type bool
        if typeCondExpr != "bool":
            error_message_ast(self.cond_expr.line, self.cond_expr.col, "If conditional expression must be of type bool", file_name, error_buffer)
        # If then
        if self.else_expr == "" :
            return "unit"
        # If then else
        else:
            # Check type for then expr
            typeElseExpr = self.else_expr.checkExpr(gst, st, file_name, error_buffer)
            # If one expr has unit type, if has unit type
            if (typeThenExpr == "unit") or (typeElseExpr == "unit"):
                return "unit"
            # Types are both primitives
            elif isPrimitive(typeThenExpr) and isPrimitive(typeElseExpr):
                # Check that both types are equal
                if typeThenExpr == typeElseExpr:
                    return typeThenExpr
            # They are both of class type
            elif not (isPrimitive(typeThenExpr) or isPrimitive(typeElseExpr)):
                # Return the first common ancestor
                return gst.commonAcenstor(typeThenExpr, typeElseExpr)

        # Error recovery
        error_message_ast(self.line, self.col, "The type of the expression inside then (" + typeThenExpr + ") does not agree with expression inside else (" + typeElseExpr + ")", file_name, error_buffer)
        return "unit"

class Expr_while(Expr):
    def __init__(self, cond_expr, body_expr):
        Node.__init__(self)
        self.cond_expr = cond_expr
        self.body_expr = body_expr

    def __str__(self):
        return get_object_string("While", [self.cond_expr, self.body_expr])

class Expr_let(Expr):
    def __init__(self, name, type, scope_expr):
        Node.__init__(self)
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
        Node.__init__(self)
        self.name = name
        self.expr = expr
    def __str__(self):
        return get_object_string("Assign", [self.name, self.expr])

    # Check expression of assign and that it does not assign to self
    def checkExpr(self, gst, st, file_name, error_buffer):
        if self.name == "self":
            error_message_ast(self.line, self.col, "cannot assign to self")


class Expr_UnOp(Expr):
    def __init__(self, unop, expr):
        Node.__init__(self)
        self.unop = unop
        self.expr = expr
    def __str__(self):
        return get_object_string("UnOp", [self.unop, self.expr])

class Expr_BinOp(Expr):
    def __init__(self, op, left_expr, right_expr):
        Node.__init__(self)
        self.op = op
        self.left_expr = left_expr
        self.right_expr = right_expr
    def __str__(self):
        return get_object_string("BinOp", [self.op, self.left_expr, self.right_expr])

class Expr_Call(Expr):
    def __init__(self, method_name, expr_list):
        Node.__init__(self)
        self.object_expr = "self"
        self.method_name = method_name
        self.expr_list = expr_list
    def __str__(self):
        return get_object_string("Call", [self.object_expr, self.method_name, self.expr_list])
    def add_object_expr(self, expr):
        self.object_expr = expr

class Expr_Object_identifier(Expr):
    def __init__(self, name):
        Node.__init__(self)
        self.name = name
    def __str__(self):
        return self.name.__str__()

class Expr_New(Expr):
    def __init__(self, type_name):
        Node.__init__(self)
        self.type_name = type_name
    def __str__(self):
        return get_object_string("New", [self.type_name])
    # Check that the type is valid
    def checkExpr(self, gst, st, file_name, error_buffer):
        return self.type_name

class Expr_Unit(Expr):
    def __init__(self):
        Node.__init__(self)
        self.unit = "()"
    def __str__(self):
        return self.unit.__str__()

    def checkExpr(self, gst, st, file_name, error_buffer):
        return "unit"

class Args(Node):
    def __init__(self):
        Node.__init__(self)
        self.list_args = []
    def __str__(self):
        return get_list_string(self.list_args)
    def add_arg(self, arg):
        self.list_args.append(arg)

class Literal(Node):
    def __init__(self, literal):
        Node.__init__(self)
        self.literal = literal

    def __str__(self):
        str = self.literal.__str__()
        return str

    # Check expression of literal
    def checkExpr(self, gst, st, file_name, error_buffer):
        if isinstance(self.literal, int):
            return "int32"
        elif isinstance(self.literal, str):
            return "string"
        else:
            return "bool"

class Boolean_literal(Node):
    def __init__(self, bool):
        Node.__init__(self)
        self.bool = bool

    def __str__(self):
        if(self.bool):
            str = "true"
        else:
            str = "false"
        return str

### General Functions
# Create a symbol table
class symbolTable():
    def __init__(self):
        self.list_context = [{}]
        self.nbr_context = 1;

    # Enter a context
    def enter_ctx(self):
        self.list_context.append({})
        self.nbr_context += 1

    # Bind a key to some info
    def bind(self, key, info):
        self.list_context[self.nbr_context-1][key] = info

    # Exit a context
    def exit_ctx(self):
        self.list_context.pop()
        self.nbr_context -= 1

    # Look up for a key in the symbol table and retreive info,
    # return None if the key is not found
    def lookup(self, key):
        return self.list_context[self.nbr_context-1].get(key)

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

# Check if a type name is primitive or not
def isPrimitive(typeName):
    return ((typeName == "int32") or (typeName == "bool") or (typeName == "string") or (typeName == "unit"))

### Error message functions
# Generate error message
def error_message_node_ast(node, description, file_name, error_buffer):
    # Generate the text of the error
    error_str = file_name + ":" + str(node.line)
    error_str += ":" + str(node.col)
    error_str += ": semantic error : " + description + "\n"

    # Add it to the buffer
    error_buffer.put(((node.line, node.col), error_str))

# Generate error message for a class
def error_message_ast(line, col, description, file_name, error_buffer):
    # Generate the text of the error
    error_str = file_name + ":" + str(line)
    error_str += ":" + str(col)
    error_str += ": semantic error : " + description + "\n"

    # Add it to the buffer
    error_buffer.put(((line, col), error_str))
