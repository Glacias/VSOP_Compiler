from llvmlite import ir

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

    # Generate code for the program
    def codeGen(self, lgen):
        # For every class
        for cl in self.list_class:
            # Generate the code
            cl.codeGen(lgen)


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
            fl.checkTypeField(gst, file_name, error_buffer)
        # Create the self Type
        selfType = Type(self.name)
        selfType.add_position(self.nameLine, self.nameCol)
        # For every method
        for mt in self.methods:
            mt.checkTypeMethod(gst, selfType, file_name, error_buffer)

    # Generate code for the class
    def codeGen(self, lgen):
        # Create init

        # For every field
        for fl in self.fields:
            fl.codeGen(lgen, self.name)

        # Create new

        # For every method
        for mt in self.methods:
            mt.codeGen(lgen, self.name)


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

    # Check the type of initializer expression
    def checkTypeField(self, gst, file_name, error_buffer):
        if self.init_expr != "":
            # Create a symbol table
            st = symbolTable()
            # Check the expression
            typeExpr = self.init_expr.checkExpr(gst, st, file_name, error_buffer)
            # Check that the initializer type corresponds to the field type
            if not gst.areConform(typeExpr, self.type.type):
                error_message_ast(self.type.line, self.type.col, "the type of the initializer (" + typeExpr + ") must conform to the declared type of the field (" + self.type.type + ")", file_name, error_buffer)

    # Generate code for the field
    def codeGen(self, lgen, className):
        pass

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

    # Check the type of the block
    def checkTypeMethod(self, gst, classNameType, file_name, error_buffer):
        # Check that the declared type is valid
        if not isPrimitive(self.type.type):
            # Check that class type is valid
            classInfo = gst.lookupForClass(self.type.type)
            if classInfo is None:
                error_message_ast(self.type.line, self.type.col, "unknown type " + self.type.type, file_name, error_buffer)
                self.type.type = "Object" # Error recovery
        # Create a symbol table
        st = symbolTable()
        # Add self
        st.bind("self", classNameType)
        # Get class info
        classInfo = gst.lookupForClass(classNameType.type)
        ## Add the fields (also ancestor fields)
        # For every ancestor (including itself)
        for clName in classInfo[3]:
            # Get the ancestor info
            anceClassInfo = gst.lookupForClass(clName)
            # Add the fields
            for fl in anceClassInfo[0].fields:
                st.bind(fl.name, fl.type)
        ## Add the formals
        methodInfo = classInfo[2].get(self.name)
        st.update(methodInfo[1])
        # Check the type of the block
        typeBlock = self.block.checkExpr(gst, st, file_name, error_buffer)
        # Check that it conform the declared type
        if not gst.areConform(typeBlock, self.type.type):
            error_message_ast(self.type.line, self.type.col, "the type of the method's body (" + typeBlock + ") must conform to the declared type of the method (" + self.type.type + ")", file_name, error_buffer)

    # Generate code for the method
    def codeGen(self, lgen, className):
        # Get the class init info
        clInitDictInfo = lgen.initDict.get(className)
        # Get the method info
        metInitDictInfo = clInitDictInfo[3][self.name]
        # Get the method declaration and create the first block
        block = metInitDictInfo[2].append_basic_block()
        # Create the builder on that block
        bldr = ir.IRBuilder(block)

        # Create a symbol table for the arguments and fields (and self)
        st = symbolTable()

        # Launch the builder on the block
        value = self.block.codeGenExpr(lgen, className, bldr, st)

        # Return the value
        bldr.ret(value)


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
            # In case the type was checked print it
            if self.typeChecked != "":
                str += " : " + self.typeChecked
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

    # Generate code for a block
    def codeGenExpr(self, lgen, className, bldr, st):
        # Open a new context
        st.enter_ctx()
        # Generate the code for all the expr
        for exp in self.list_expr:
            value = exp.codeGenExpr(lgen, className, bldr, st)
        # Exit the context
        st.exit_ctx()
        # Return the value of the last expr
        return value

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
        # In case the type was checked print it
        if self.typeChecked != "":
            str += " : " + self.typeChecked
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
            error_message_ast(self.cond_expr.line, self.cond_expr.col, "IF conditional expression must be of type bool", file_name, error_buffer)
        # If then
        if self.else_expr == "" :
            self.typeChecked = "unit"
            return self.typeChecked
        # If then else
        else:
            # Check type for then expr
            typeElseExpr = self.else_expr.checkExpr(gst, st, file_name, error_buffer)
            # If one expr has unit type, if has unit type
            if (typeThenExpr == "unit") or (typeElseExpr == "unit"):
                self.typeChecked = "unit"
                return self.typeChecked
            # Types are both primitives
            elif isPrimitive(typeThenExpr) and isPrimitive(typeElseExpr):
                # Check that both types are equal
                if typeThenExpr == typeElseExpr:
                    self.typeChecked = typeThenExpr
                    return self.typeChecked
            # They are both of class type
            elif not (isPrimitive(typeThenExpr) or isPrimitive(typeElseExpr)):
                # Return the first common ancestor
                self.typeChecked = gst.commonAcenstor(typeThenExpr, typeElseExpr)
                return self.typeChecked

        # Error recovery
        error_message_ast(self.line, self.col, "IF conditional expression, the type of the expression inside THEN (" + typeThenExpr + ") does not agree with the type of the expression inside ELSE (" + typeElseExpr + ")", file_name, error_buffer)
        return "unit"

class Expr_while(Expr):
    def __init__(self, cond_expr, body_expr):
        Node.__init__(self)
        self.cond_expr = cond_expr
        self.body_expr = body_expr

    def __str__(self):
        str = get_object_string("While", [self.cond_expr, self.body_expr])
        # In case the type was checked print it
        if self.typeChecked != "":
            str += " : " + self.typeChecked
        return str

    # Check the expressions of while
    def checkExpr(self, gst, st, file_name, error_buffer):
        # Check type of expr
        typeCondExpr = self.cond_expr.checkExpr(gst, st, file_name, error_buffer)
        typeBodyExpr = self.body_expr.checkExpr(gst, st, file_name, error_buffer)
        # Check that cond expr is type bool
        if typeCondExpr != "bool":
            error_message_ast(self.cond_expr.line, self.cond_expr.col, "while conditional expression must be of type bool", file_name, error_buffer)
        self.typeChecked = "unit"
        return self.typeChecked

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
        # In case the type was checked print it
        if self.typeChecked != "":
            str += " : " + self.typeChecked
        return str

    # Add init expr
    def add_init_expr(self, init_expr):
        self.init_expr = init_expr

    # Check the expressions of let
    def checkExpr(self, gst, st, file_name, error_buffer):
        # Check that the type is valid
        if not isPrimitive(self.type.type):
            # Check that class type is valid
            classInfo = gst.lookupForClass(self.type.type)
            if classInfo is None:
                error_message_ast(self.type.line, self.type.col, "unknown type " + self.type.type, file_name, error_buffer)
                self.type.type = "Object" # Error recovery

        # if let assign in
        if self.init_expr != "":
            # Look at the type of the initializer
            typeInitExpr = self.init_expr.checkExpr(gst, st, file_name, error_buffer)
            # Check that it conforms the type
            if not gst.areConform(typeInitExpr, self.type.type):
                error_message_ast(self.init_expr.line, self.init_expr.col, "the type of the initializer (" + typeInitExpr + ") must conform to the declared type of the let (" + self.type.type + ")", file_name, error_buffer)

        # Check that self is not the name of the identifier
        if self.name == "self":
            error_message_ast(self.line, self.col, "bound identifier cannot be named self", file_name, error_buffer)
            # Error recovery

        # Create a new context
        st.enter_ctx()
        # Bind the identifier and type
        st.bind(self.name, self.type)
        # Check the type of the scope
        self.typeChecked = self.scope_expr.checkExpr(gst, st, file_name, error_buffer)
        # Exit the context
        st.exit_ctx()
        return self.typeChecked


class Expr_assign(Expr):
    def __init__(self, name, expr):
        Node.__init__(self)
        self.name = name
        self.expr = expr
    def __str__(self):
        str = get_object_string("Assign", [self.name, self.expr])
        # In case the type was checked print it
        if self.typeChecked != "":
            str += " : " + self.typeChecked
        return str

    # Check expression of assign and that it does not assign to self
    def checkExpr(self, gst, st, file_name, error_buffer):
        # Check it does not assign to self
        if self.name == "self":
            error_message_ast(self.line, self.col, "cannot assign to self", file_name, error_buffer)
        # Get the type of identifier
        infoId = st.lookup(self.name)
        # Check it exist
        if infoId is None:
            error_message_ast(self.line, self.col, "unknown variable " + self.name, file_name, error_buffer)
            return "Object" # Error recovery
        # Check the type of the expr
        typeExpr = self.expr.checkExpr(gst, st, file_name, error_buffer)
        # Check that types are conform
        if not gst.areConform(typeExpr, infoId.type):
            error_message_ast(self.line, self.col, "cannot assign identifier " + self.name + " with declared type (" + infoId.type + ") as assigned expression type (" + typeExpr + ") does not conform", file_name, error_buffer)
            return infoId.type # Error recovery
        self.typeChecked = infoId.type
        return self.typeChecked

class Expr_UnOp(Expr):
    def __init__(self, unop, expr):
        Node.__init__(self)
        self.unop = unop
        self.expr = expr
    def __str__(self):
        str = get_object_string("UnOp", [self.unop, self.expr])
        # In case the type was checked print it
        if self.typeChecked != "":
            str += " : " + self.typeChecked
        return str

    # Check expression of unary operator
    def checkExpr(self, gst, st, file_name, error_buffer):
        # Check type of expr
        typeExpr = self.expr.checkExpr(gst, st, file_name, error_buffer)
        # if unop is "not" check for bool
        if self.unop == "not":
            if typeExpr != "bool":
                error_message_ast(self.line, self.col, "unary operator NOT, expression must be of type bool", file_name, error_buffer)
                return "bool" # Error recovery : bool
            self.typeChecked = "bool"
        # if unop is minus check for int32
        elif self.unop == "-":
            if typeExpr != "int32":
                error_message_ast(self.line, self.col, "unary MINUS operator, expression must be of type int32", file_name, error_buffer)
                return "int32" # Error recovery : int32
            self.typeChecked = "int32"
        # if unop is isnull check for class type
        else:
            if isPrimitive(typeExpr):
                error_message_ast(self.line, self.col, "unary ISNULL operator, expression must be of type Object", file_name, error_buffer)
                return "bool" # Error recovery : bool
            self.typeChecked = "bool"
        return self.typeChecked

class Expr_BinOp(Expr):
    def __init__(self, op, left_expr, right_expr):
        Node.__init__(self)
        self.op = op
        self.left_expr = left_expr
        self.right_expr = right_expr
    def __str__(self):
        str = get_object_string("BinOp", [self.op, self.left_expr, self.right_expr])
        # In case the type was checked print it
        if self.typeChecked != "":
            str += " : " + self.typeChecked
        return str

    # Check expression of binary operator
    def checkExpr(self, gst, st, file_name, error_buffer):
        # Check type of both expr
        typeLeftExpr = self.left_expr.checkExpr(gst, st, file_name, error_buffer)
        typeRightExpr = self.right_expr.checkExpr(gst, st, file_name, error_buffer)
        # And
        if self.op ==  "and":
            # Check that both type are bool
            if (typeLeftExpr != "bool") or (typeRightExpr != "bool"):
                error_message_ast(self.line, self.col, "binary operator AND, expressions must be of type bool", file_name, error_buffer)
                return "bool"
            else:
                self.typeChecked = "bool"
                return self.typeChecked

        # Equal
        elif self.op == "=":
            # Types are both primitives
            if isPrimitive(typeLeftExpr) and isPrimitive(typeRightExpr):
                # Check that both types are equal
                if typeLeftExpr != typeRightExpr:
                    error_message_ast(self.line, self.col, "binary operator =, for primitive types, types of expression must be identical", file_name, error_buffer)
                    return "bool"
                else:
                    self.typeChecked = "bool"
                    return self.typeChecked
            # They are both of class type
            elif not (isPrimitive(typeLeftExpr) or isPrimitive(typeRightExpr)):
                self.typeChecked = "bool"
                return self.typeChecked
            else:
                error_message_ast(self.line, self.col, "binary operator =, types of expression must be identical", file_name, error_buffer)
                return "bool"

        # Lower
        elif self.op == "<":
            # Check that both type are int32
            if (typeLeftExpr != "int32") or (typeRightExpr != "int32"):
                error_message_ast(self.line, self.col, "binary operator <, expressions must be of type int32", file_name, error_buffer)
                return "bool"
            else:
                self.typeChecked = "bool"
                return self.typeChecked

        # Lower equal
        elif self.op == "<=":
            # Check that both type are int32
            if (typeLeftExpr != "int32") or (typeRightExpr != "int32"):
                error_message_ast(self.line, self.col, "binary operator <=, expressions must be of type int32", file_name, error_buffer)
                return "bool"
            else:
                self.typeChecked = "bool"
                return self.typeChecked

        # Plus
        elif self.op == "+":
            # Check that both type are int32
            if (typeLeftExpr != "int32") or (typeRightExpr != "int32"):
                error_message_ast(self.line, self.col, "binary operator +, expressions must be of type int32", file_name, error_buffer)
                return "int32"
            else:
                self.typeChecked = "int32"
                return self.typeChecked

        # Minus
        elif self.op == "-":
            # Check that both type are int32
            if (typeLeftExpr != "int32") or (typeRightExpr != "int32"):
                error_message_ast(self.line, self.col, "binary operator -, expressions must be of type int32", file_name, error_buffer)
                return "int32"
            else:
                self.typeChecked = "int32"
                return self.typeChecked

        # Times
        elif self.op == "*":
            # Check that both type are int32
            if (typeLeftExpr != "int32") or (typeRightExpr != "int32"):
                error_message_ast(self.line, self.col, "binary operator *, expressions must be of type int32", file_name, error_buffer)
                return "int32"
            else:
                self.typeChecked = "int32"
                return self.typeChecked

        # Div
        elif self.op == "/":
            # Check that both type are int32
            if (typeLeftExpr != "int32") or (typeRightExpr != "int32"):
                error_message_ast(self.line, self.col, "binary operator /, expressions must be of type int32", file_name, error_buffer)
                return "int32"
            else:
                self.typeChecked = "int32"
                return self.typeChecked

        # Pow
        elif self.op == "^":
            # Check that both type are int32
            if (typeLeftExpr != "int32") or (typeRightExpr != "int32"):
                error_message_ast(self.line, self.col, "binary operator ^, expressions must be of type int32", file_name, error_buffer)
                return "int32"
            else:
                self.typeChecked = "int32"
                return self.typeChecked

        # Something went wrong
        else:
            error_message_ast(self.line, self.col, "Failed to recognise binary operator", file_name, error_buffer)
            return "bool"

class Expr_Call(Expr):
    def __init__(self, method_name, args):
        Node.__init__(self)
        self.object_expr = "self"
        self.method_name = method_name
        self.args = args
    def __str__(self):
        str = get_object_string("Call", [self.object_expr, self.method_name, self.args])
        # In case the type was checked print it
        if self.typeChecked != "":
            str += " : " + self.typeChecked
        return str
    def add_object_expr(self, expr):
        self.object_expr = expr

    # Check the type of the call
    def checkExpr(self, gst, st, file_name, error_buffer):
        # In case of deduced self, check the type of self
        if self.object_expr == "self":
            # Check that self is in scope
            selfInfo = st.lookup("self")
            if selfInfo is None:
                error_message_ast(self.line, self.col, "cannot access self inside field initializer", file_name, error_buffer)
                return "Object" # Error recovery
            else:
                # Create the self
                selfExpr = Expr_Object_identifier("self")
                selfExpr.add_position(self.line,self.col)
                selfExpr.typeChecked = selfInfo.type
                # Change the expression object expr to self
                self.object_expr = selfExpr
                # Get the type of the object expr
                typeObjectExpr = selfInfo.type
        else:
            # Check the type of the object expr
            typeObjectExpr = self.object_expr.checkExpr(gst, st, file_name, error_buffer)

        # Check that the identifier as a class type
        if isPrimitive(typeObjectExpr):
            error_message_ast(self.line, self.col, "cannot call on a primitive type", file_name, error_buffer)
            return "Object" # Error recovery

        # Get class info
        classInfo = gst.lookupForClass(typeObjectExpr)
        # Check that class info exist
        if classInfo is None:
            #error_message_ast(self.line, self.col, "called on invalid object (probably self)", file_name, error_buffer)
            # currently catches wrong self. in field
            return "Object" # Error recovery

        # Get method info
        methodInfo = gst.lookupMethodsAncestors(classInfo[0], self.method_name)[0]
        # Check that the method exist for that class type (also in the ancestor)
        if methodInfo is None:
            error_message_ast(self.line, self.col, "class " + typeObjectExpr + " has no method called " + self.method_name, file_name, error_buffer)
            return "Object" # Error recovery

        # Get the arguments and formals
        list_arg = self.args.list_args
        list_formals = methodInfo[0].formals.list_formals

        # First check that there is the same number of args and formals
        if len(list_arg) != len(list_formals):
            error_message_ast(self.line, self.col, "method " + self.method_name + " takes " + str(len(list_formals)) + " argument but " + str(len(list_arg)) + " were given", file_name, error_buffer)

        # Check that arguments are the same type (order maters)
        for i in range(len(list_arg)):
            # Check type of argument
            typeArg = list_arg[i].checkExpr(gst, st, file_name, error_buffer)
            # Check that types are conform
            if not gst.areConform(typeArg, list_formals[i].type.type):
                error_message_ast(list_arg[i].line, list_arg[i].col, "argument " + list_formals[i].name + " (at position " + str(i+1) + ") should conform type " + list_formals[i].type.type + " (currently is of type " + typeArg + ")", file_name, error_buffer)

        self.typeChecked = methodInfo[0].type.type
        return self.typeChecked

class Expr_Object_identifier(Expr):
    def __init__(self, name):
        Node.__init__(self)
        self.name = name
    def __str__(self):
        str = self.name.__str__()
        # In case the type was checked print it
        if self.typeChecked != "":
            str += " : " + self.typeChecked
        return str
    # Check that the variable exist
    def checkExpr(self, gst, st, file_name, error_buffer):
        # Look for variable
        varInfo = st.lookup(self.name)
        if varInfo is None:
            if self.name == "self":
                error_message_ast(self.line, self.col, "cannot access self inside field initializer", file_name, error_buffer)
            else:
                error_message_ast(self.line, self.col, "unknown variable " + self.name, file_name, error_buffer)
                return "Object" # Error recovery
        else:
            self.typeChecked = varInfo.type
            return self.typeChecked

class Expr_New(Expr):
    def __init__(self, type_name):
        Node.__init__(self)
        self.type_name = type_name
    def __str__(self):
        str = get_object_string("New", [self.type_name])
        # In case the type was checked print it
        if self.typeChecked != "":
            str += " : " + self.typeChecked
        return str
    # Check that the class type is valid
    def checkExpr(self, gst, st, file_name, error_buffer):
        # Look for class
        classInfo = gst.lookupForClass(self.type_name)
        if classInfo is None:
            error_message_ast(self.line, self.col, "unknown type " + self.type_name, file_name, error_buffer)
            return "Object" # Error recovery
        else:
            self.typeChecked = self.type_name
            return self.typeChecked

class Expr_Unit(Expr):
    def __init__(self):
        Node.__init__(self)
        self.unit = "()"
    def __str__(self):
        str = self.unit.__str__()
        # In case the type was checked print it
        if self.typeChecked != "":
            str += " : " + self.typeChecked
        return str
    def checkExpr(self, gst, st, file_name, error_buffer):
        self.typeChecked = "unit"
        return self.typeChecked

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
        # In case the type was checked print it
        if self.typeChecked != "":
            str += " : " + self.typeChecked
        return str
    # Check expression of literal
    def checkExpr(self, gst, st, file_name, error_buffer):
        if isinstance(self.literal, int):
            self.typeChecked = "int32"
            return self.typeChecked
        elif isinstance(self.literal, str):
            self.typeChecked = "string"
            return self.typeChecked
        else:
            self.typeChecked = "bool"
            return self.typeChecked

    # Generate code for a literal
    def codeGenExpr(self, lgen, className, bldr, st):
        # int
        if isinstance(self.literal, int):
            return lgen.int32(self.literal)

        # str
        elif isinstance(self.literal, str):
            # Add the null char at the end
            string1 = self.literal[1:-1] + '\0'

            # Create a global constant
            c_string1 = ir.Constant(ir.ArrayType(ir.IntType(8), len(string1)), bytearray(string1.encode("utf8")))
            global_string1 = ir.GlobalVariable(lgen.module, c_string1.type, name=("str" + str(lgen.nbrStr)))
            lgen.nbrStr = lgen.nbrStr + 1
            global_string1.linkage = ''
            global_string1.global_constant = True
            global_string1.initializer = c_string1

            # Return a pointer to the global constant
            pt = bldr.gep(global_string1, [lgen.int32(0), lgen.int32(0)], inbounds=True)
            return pt

        # bool
        else:
            if self.literal.bool == "true":
                return lgen.bool(1)
            else:
                return lgen.bool(0)


class Boolean_literal(Node):
    def __init__(self, bool):
        Node.__init__(self)
        self.bool = bool
    def __str__(self):
        if(self.bool):
            str = "true"
        else:
            str = "false"
        # In case the type was checked print it
        if self.typeChecked != "":
            str += " : " + self.typeChecked
        return str
    # Check expression of literal
    def checkExpr(self, gst, st, file_name, error_buffer):
        self.typeChecked = "bool"
        return self.typeChecked

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
        info = self.list_context[self.nbr_context-1].get(key)
        nbrCtx = self.nbr_context-1
        while (info is None) and (nbrCtx>=0):
            info = self.list_context[nbrCtx-1].get(key)
            nbrCtx = nbrCtx-1
        return info

    # Update the context with the content of a dictonnary
    def update(self, dict):
        self.list_context[self.nbr_context-1].update(dict)

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
