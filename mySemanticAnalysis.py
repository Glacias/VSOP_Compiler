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
    global typesOfType
    typesOfType = {"int32", "bool", "string", "unit"}

    # Make global symbol table and add all classes to it
    gst = globalSymbolTable()

    # Add the Object class
    gst.add_class(class_Object())

    # For every class
    for cl in ast.list_class:
        # Adding a class also checks :
        # - that a class or more were not already defined (+ special case for Object)
        # - that a field was not defined twice in the same class
        # - that a field is not named self
        # - that a method was not defined twice in the same class
        # - that a method's formals were not defined twice or named to self
        gst.add_class(cl)
        typesOfType.add(cl.name) # Add the class name as a new type of type

    # If errors were detected, exit
    if not error_buffer.empty():
        terminate()

    # Check for cycles in class inheritance and check that parent are defined
    checkForCycle(ast, gst)

    # Check that a child's field does not overide a parent's field
    checkFieldsMethodsAndFormals(ast, gst)



    # If errors were detected, exit
    if not error_buffer.empty():
        terminate()

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
                    # Add the field (stored info is the field)
                    dictFields[field_class.name] = field_class

            # Fill methods
            for method_class in node_class.methods:
                # Check for already defined fields
                if method_class.name in dictMethods:
                    # Write the error
                    oldMethod = dictMethods[method_class.name]
                    error_message(method_class.line, method_class.col, "field " + method_class.name + " was already defined at " + str(oldMethod.line) + ":" + str(oldMethod.col) + ".")
                else:
                    # Create a dictonnary for formals
                    dictFormals = {}

                    # Fill formals
                    for formal_class in method_class.formals.list_formals:
                        # Check for already defined fields
                        if formal_class.name in dictFormals:
                            # Write the error
                            oldFormal = dictFormals[formal_class.name]
                            error_message(formal_class.line, formal_class.col, "redefinition of formal parameter " + formal_class.name + ",\n    first defined at " + str(oldFormal.line) + ":" + str(oldFormal.col) + ".")
                        # Check for a field named self
                        elif formal_class.name == "self":
                            error_message(formal_class.line, formal_class.col, "A formal parameter cannot be named self.")
                        else:
                            # Add the formal (stored info is the type)
                            dictFormals[formal_class.name] = formal_class.type

                    # Add the method with formals
                    # (stored info is the method and dictonnary of formals)
                    dictMethods[method_class.name] = (method_class, dictFormals)

            # Add the class with fields and methods
            # (stored info is the class, dictonnary of fields and dictonnary of methods)
            self.class_table[node_class.name] = (node_class, dictFields, dictMethods);

    # Look for a class and return the info and None if the class is not there
    def lookupForClass(self, className):
        return self.class_table.get(className)

    # Look up for a field in a class and the ancestors of that class
    # Return info or None if field not found
    def lookupFieldsAncestors(self, cl, fieldName):
        # Get the info of the class
        classInfo = self.lookupForClass(cl.name)
        # Look inside the class fields
        fieldInfo = classInfo[1].get(fieldName)
        # If field not found, look in parents
        # Stop at Object since it has no fields
        if fieldInfo is None and cl.parent != "Object":
            parentInfo = self.lookupForClass(cl.parent)
            # Recursive call in order to look at all ancestors
            return self.lookupFieldsAncestors(parentInfo[0], fieldName)
        else:
            return (fieldInfo, cl.name)


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


# Check that a child's field does not overide a parent's field
#  and that types in field, methods and formals exist
def checkFieldsMethodsAndFormals(ast, gst):
    # For every class
    for cl in ast.list_class:
        # Check that it has a parent
        if cl.parent != "Object":
            # For every field in the class
            for fl in cl.fields:
                # Get the info for field in the ancestors
                parentInfo = gst.lookupForClass(cl.parent)
                fieldInfo = gst.lookupFieldsAncestors(parentInfo[0], fl.name)
                # If the info is not None, redefinition of field
                if fieldInfo[0] is not None:
                    error_message(fl.line, fl.col, "redefinition of field " + fl.name + ", \n    first defined in parent class " + fieldInfo[1] + " at " + str(fieldInfo[0].line) + ":" + str(fieldInfo[0].col))
                # Check that field type exist
                if not typeExist(fl.type):
                    error_message(fl.line, fl.col, "unknown type " + fl.type.type)
        else:
            # For every field in the class
            for fl in cl.fields:
                # Check that field type exist
                if not typeExist(fl.type):
                    error_message(fl.line, fl.col, "unknown type " + fl.type.type)

        # For every method in the class
        for mt in cl.methods:
            # Check that method type exist
            if not typeExist(mt.type):
                error_message(mt.line, mt.col, "unknown type " + mt.type.type)
            # For every formal in method
            for fm in mt.formals.list_formals:
                # Check that formal type exist
                if not typeExist(fm.type):
                    error_message(fm.line, fm.col, "unknown type " + fm.type.type)

    # If errors were detected, exit
    if not error_buffer.empty():
        terminate()


# Check that a type exist
def typeExist(type_class):
    if type_class.type in typesOfType:
        return True
    else:
        return False

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
