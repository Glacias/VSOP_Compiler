# -----------------------------------------------------------------------------
# mySemanticAnalysis.py
#
# File responsible for the syntax analysis
# Made by Simon Bernard and Ivan Klapka for the Project 1 : lexical analysis
# University of Liège - Academic year 2019-2020 - INFO0085-1 Compilers course
# -----------------------------------------------------------------------------
import sys
import queue
from myAST import *

def checkSemantic(ast, file):
    global file_name
    file_name = file # Save the file name for error reporting
    global error_buffer
    error_buffer = queue.PriorityQueue() # Create the error buffer

    # Make global symbol table and add all classes to it
    gst = globalSymbolTable()

    # Add the Object class
    gst.add_class(class_Object())

    for cl in ast.list_class:
        # Adding a class checks :
        # - that a class or more were not already defined (+ special case for Object)
        # - that a method was not defined twice in the same class
        # - that a field was not defined twice in the same class
        # - that a field name is not equal to "self"
        gst.add_class(cl)

    # If errors were detected, exit
    if not error_buffer.empty():
        terminate()

    # Check for cycles in class inheritance and check that parent are defined
    checkForCycle(ast, gst)

    # Check that a child's field does not overide a parent's field


    return ast


# Create a global symbol table
class globalSymbolTable():
    def __init__(self):
        self.class_table = {}
        self.nbr_class = 0;

    # Add a class to the table (with its fields and methods)
    def add_class(self, node_class):
        # Check for already defined class
        if node_class.name in self.class_table:
            # Send an error
            # If redefined class is Object
            if node_class.name == "Object":
                error_message(node_class.nameLine, node_class.nameCol, "redefinition of predefined class Object is not allowed")
            else:
                oldClass = self.class_table[node_class.name][0]
                error_message(node_class.nameLine, node_class.nameCol, "redefinition of class " + node_class.name + ",\n    first defined at " + str(oldClass.nameLine) + ":" + str(oldClass.nameCol) + ".")
        else:
            # Create a dictonnary for fields and methods
            dictFields = {}
            dictMethods = {}

            # Fill fields
            for field_class in node_class.fields:
                # Check for already defined fields
                if field_class.name in dictFields:
                    # Write the error
                    oldField = dictFields[field_class.name]
                    error_message(field_class.line, field_class.col, "redefinition of field " + field_class.name + ",\n    first defined at " + str(oldField.line) + ":" + str(oldField.col) + ".")
                # Check for a field named self
                elif field_class.name == "self":
                    error_message(field_class.line, field_class.col, "A field cannot be named self.")
                else:
                    # Add the field
                    dictFields[field_class.name] = field_class

            # Fill methods
            for method_class in node_class.methods:
                # Check for already defined fields
                if method_class.name in dictMethods:
                    # Write the error
                    oldMethod = dictMethods[method_class.name]
                    error_message(method_class.line, method_class.col, "field " + method_class.name + " was already defined at " + str(oldMethod.line) + ":" + str(oldMethod.col) + ".")
                else:
                    # Add the method
                    dictMethods[method_class.name] = method_class

            # Add the class
            self.class_table[node_class.name] = [node_class, dictFields, dictMethods];

    # Look for a class and return the info and None if the class is not there
    def lookupForClass(self, className):
        return self.class_table.get(className)


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


# Check for cycles in class inheritance
def checkForCycle(ast, gst):
    # Create an empty set for node checked
    class_checked = set()
    # Add Object to node checked
    class_checked.add("Object")
    # For each class
    for cl in ast.list_class:
        className = cl.name
        # If the class has not already been checked
        if not (className in class_checked):
            # Create an empty set for node seen
            class_seen = set()
            # Add the current class name
            class_seen.add(className)
            current_class = cl
            # Go up the inheritance and look for already seen node
            while(current_class.parent != "Object"):
                current_class_name = current_class.parent
                next_class = gst.lookupForClass(current_class_name)
                # Check that the parent parent is defined
                if next_class is None :
                    error_message(current_class.parentLine, current_class.parentCol, "class " + current_class.name + " cannot extend class " + current_class.parent + ",\n    " + current_class.parent + " was not defined.")
                    break;
                current_class = next_class[0]
                # If the node has already been checked
                if current_class_name in class_checked:
                    # We know it will not cycle
                    break
                # If the node has already been seen
                elif current_class_name in class_seen:
                    # Cycle in inheritance
                    # Generate error messages
                    for clname in class_seen:
                        cl = gst.lookupForClass(clname)[0]
                        error_message(cl.parentLine, cl.parentCol, "class " + cl.name + " cannot extend child class " + cl.parent + ".")
                    # Exit
                    terminate()
                else:
                # Add the class to the seen set
                    class_seen.add(current_class_name)

            # Once we reached Object, all nodes seen become checked
            class_checked = class_checked|class_seen
    # If errors were detected, exit
    if not error_buffer.empty():
        terminate()


# Create the class Object
def class_Object():
    # Initialise Class
    obj = Class()
    obj.change_name("Object")
    obj.change_parent("")
    obj.add_position_name(0,0)
    obj.add_position_parent(0,0)

    ## Add predefined methods
    # print
    printF1 = Formal("s", "string")
    printFormals = Formals()
    printFormals.add_formal(printF1)
    print = Method("print", printFormals, "Obejct", "{ (* print s on stdout, then return self *) }")
    obj.add_method(print)

    # printBool
    printBoolF1 = Formal("b", "bool")
    printBoolFormals = Formals()
    printBoolFormals.add_formal(printBoolF1)
    printBool = Method("printBool", printBoolFormals, "Obejct", "{ (* print b on stdout, then return self *) }")
    obj.add_method(printBool)

    # printInt32
    printInt32F1 = Formal("i", "int32")
    printInt32Formals = Formals()
    printInt32Formals.add_formal(printInt32F1)
    printInt32 = Method("printInt32", printInt32Formals, "Obejct", "{ (* print b on stdout, then return self *) }")
    obj.add_method(printInt32)

    # inputLine
    inputLine = Method("inputLine", Formals(), "string", "{ (* read one line from stdin, return \"\" in case of error *) }")
    obj.add_method(inputLine)

    # inputBool
    inputBool = Method("inputBool", Formals(), "bool", "{ (* read one boolean value from stdin, exit with error message in case of error *) }")
    obj.add_method(inputBool)

    # inputLine
    inputInt32 = Method("inputInt32", Formals(), "int32", "{ (* read one integer from stdin, exit with error message in case of error *) }")
    obj.add_method(inputInt32)

    return obj

### Error message functions
# Generate error message
def error_message_node(node, description):
    # Generate the text of the error
    error_str = file_name + ":" + str(node.line)
    error_str += ":" + str(node.col)
    error_str += ": semantic error : " + description + "\n"

    # Add it to the buffer
    global error_buffer
    error_buffer.put(((node.line, node.col), error_str))

# Generate error message for a class
def error_message(line, col, description):
    # Generate the text of the error
    error_str = file_name + ":" + str(line)
    error_str += ":" + str(col)
    error_str += ": semantic error : " + description + "\n"

    # Add it to the buffer
    global error_buffer
    error_buffer.put(((line, col), error_str))

# Flush error buffer and exit
def terminate():
    global error_buffer
    while not error_buffer.empty():
        err = error_buffer.get()
        sys.stderr.write(err[1])
    sys.exit(1)
