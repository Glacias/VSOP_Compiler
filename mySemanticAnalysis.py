# -----------------------------------------------------------------------------
# mySemanticAnalysis.py
#
# File responsible for the syntax analysis
# Made by Simon Bernard and Ivan Klapka for the Project 1 : lexical analysis
# University of Liège - Academic year 2019-2020 - INFO0085-1 Compilers course
# -----------------------------------------------------------------------------
import sys
import queue

def checkSemantic(ast, file):
    global file_name
    file_name = file # Save the file name for error reporting
    global error_buffer
    error_buffer = queue.PriorityQueue() # Create the error buffer

    # Make global symbol table and add all classes to it
    gst = globalSymbolTable()
    for cl in ast.list_class:
        gst.add_class(cl)

    # If a class or more were already defined, exit
    if not error_buffer.empty():
        terminate()

    # Check for cycles in class inheritance
    checkForCycle(ast, gst)



    return ast



# Check for cycles in class inheritance
def checkForCycle(ast, gst):
    # Create an empty set for node checked
    class_checked = set()
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
                current_class = gst.lookupForClass(current_class_name)[0]
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


# Create a global symbol table
class globalSymbolTable():
    def __init__(self):
        self.class_table = {}
        self.nbr_class = 0;

    # Add a class to the table
    def add_class(self, node_class):
        # Check for already defined class
        if node_class.name in self.class_table:
            # Write the error
            oldClass = self.class_table[node_class.name][0]
            error_message(node_class.nameLine, node_class.nameCol, "class " + node_class.name + " was already defined at " + str(oldClass.nameLine) + ":" + str(oldClass.nameCol) + ".")
        else:
            # Add the class
            self.class_table[node_class.name] = [node_class, symbolTable(), symbolTable()];

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

### Error message functions
# Generate error message
def error_message_node(node, description):
    # Generate the text of the error
    error_str = file_name + ":" + str(node.line)
    error_str += ":" + str(node.col)
    error_str += ": semantic error :\n  " + description + "\n"

    # Add it to the buffer
    global error_buffer
    error_buffer.put(((node.line, node.col), error_str))

# Generate error message for a class
def error_message(line, col, description):
    # Generate the text of the error
    error_str = file_name + ":" + str(line)
    error_str += ":" + str(col)
    error_str += ": semantic error :\n  " + description + "\n"

    # Add it to the buffer
    global error_buffer
    error_buffer.put(((line, col), error_str))

# Flush error buffer and exit
def terminate():
    print("err")
    global error_buffer
    while not error_buffer.empty():
        err = error_buffer.get()
        sys.stderr.write(err[1])
    sys.exit(1)
