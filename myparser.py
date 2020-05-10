# -----------------------------------------------------------------------------
# myparser.py
#
# File responsible for the syntax analysis
# Made by Simon Bernard and Ivan Klapka for the Project 2 : syntax analysis
# University of Liège - Academic year 2019-2020 - INFO0085-1 Compilers course
# -----------------------------------------------------------------------------

import ply.yacc as yacc
from myAST import *
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
        # When one or more error where detected raise an error flag
        self.errFlag = False
        global file_name
        file_name = file

    # Build the parser
    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)

    ### Rules for parsing
    # In rules expression, tokens will start with a lowercase letter and rules with an uppercase letter
    def p_Program(self, p):
        '''Program : Class
                   | Program Class'''
        if(len(p)==2):
            self.ast_root.add_class(p[1])
            self.ast_root.add_position(0,0)
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
            p[0].add_position(p.lineno(1), p.lexpos(1) - p.lexer.line_end_pos_table[p.lineno(1)-1])
            p[0].add_position_name(p.lineno(2), p.lexpos(2) - p.lexer.line_end_pos_table[p.lineno(2)-1])
        else:
            p[0] = p[6]
            p[0].change_name(p[2])
            p[0].change_parent(p[4])
            p[0].add_position(p.lineno(1), p.lexpos(1) - p.lexer.line_end_pos_table[p.lineno(1)-1])
            p[0].add_position_name(p.lineno(2), p.lexpos(2) - p.lexer.line_end_pos_table[p.lineno(2)-1])
            p[0].add_position_parent(p.lineno(4), p.lexpos(4) - p.lexer.line_end_pos_table[p.lineno(4)-1])

    # General error rule for class
    def p_Class_error(self, p):
        '''Class : class type_identifier lbrace error rbrace
                 | class type_identifier extends type_identifier lbrace error rbrace'''
        error_message_line_col(p.lineno(1), p.lexpos(1) - p.lexer.line_end_pos_table[p.lineno(1)-1], "Something went wrong inside the body of class " + p[2])
        # Raise the error flag
        self.errFlag = True

    # Error rule for class when no name is given
    def p_Class_error_no_name(self, p):
        '''Class : class lbrace Class_body rbrace
                 | class extends type_identifier lbrace Class_body rbrace'''
        error_message_line_col(p.lineno(1), p.lexpos(1) - p.lexer.line_end_pos_table[p.lineno(1)-1], "Must provide a name for a class.")
        # Raise the error flag
        self.errFlag = True
        # Raise the error for the parser
        raise SyntaxError

    # Error rule for class when an object identifier is given as name
    def p_Class_error_object_id_name(self, p):
        '''Class : class object_identifier lbrace error rbrace
                 | class object_identifier extends type_identifier lbrace Class_body rbrace'''
        error_message_line_col(p.lineno(1), p.lexpos(1) - p.lexer.line_end_pos_table[p.lineno(1)-1], "Class name \"" + p[2] + "\" is incorrect, a class name must start with an uppercase letter.")
        # Raise the error flag
        self.errFlag = True
        # Raise the error for the parser
        raise SyntaxError

    # Error rule for class when an object identifier is given as name for a parent
    def p_Class_error_object_id_name_parent(self, p):
        '''Class : class type_identifier extends object_identifier lbrace Class_body rbrace'''
        error_message_line_col(p.lineno(1), p.lexpos(1) - p.lexer.line_end_pos_table[p.lineno(1)-1], "Parent class name \"" + p[4] + "\" is incorrect, a class name must start with an uppercase letter.")
        # Raise the error flag
        self.errFlag = True
        # Raise the error for the parser
        raise SyntaxError

    def p_Field(self, p):
        '''Field : object_identifier colon Type semicolon
                 | object_identifier colon Type assign Expr semicolon'''
        if(len(p)==5):
            p[0] = Field(p[1], p[3])
            p[0].add_position(p.lineno(1), p.lexpos(1) - p.lexer.line_end_pos_table[p.lineno(1)-1])
        else:
            p[0] = Field(p[1], p[3])
            p[0].add_init_expr(p[5])
            p[0].add_position(p.lineno(1), p.lexpos(1) - p.lexer.line_end_pos_table[p.lineno(1)-1])

    # Error rule for field when it is not ended with a semicolon
    def p_Field_error_semicolon(self, p):
        '''Field : object_identifier colon Type
                 | object_identifier colon Type assign Expr'''
        error_message_line_col(p.lineno(1), p.lexpos(1) - p.lexer.line_end_pos_table[p.lineno(1)-1], "Field " + p[1] + " must end with a semicolon.")
        if(len(p)==5):
            p[0] = Field(p[1], p[3])
            p[0].add_position(p.lineno(1), p.lexpos(1) - p.lexer.line_end_pos_table[p.lineno(1)-1])
        else:
            p[0] = Field(p[1], p[3])
            p[0].add_init_expr(p[5])
            p[0].add_position(p.lineno(1), p.lexpos(1) - p.lexer.line_end_pos_table[p.lineno(1)-1])
        # Raise the error flag
        self.errFlag = True

    # Error rules for field when the type is not declared
    def p_Field_error_type(self, p):
        '''Field : object_identifier semicolon
                 | object_identifier assign Expr semicolon'''
        error_message_line_col(p.lineno(1), p.lexpos(1) - p.lexer.line_end_pos_table[p.lineno(1)-1], "Must declare the type of field " + p[1])
        if(len(p)==5):
            p[0] = Field(p[1], "")
            p[0].add_position(p.lineno(1), p.lexpos(1) - p.lexer.line_end_pos_table[p.lineno(1)-1])
        else:
            p[0] = Field(p[1], "")
            p[0].add_init_expr(p[3])
            p[0].add_position(p.lineno(1), p.lexpos(1) - p.lexer.line_end_pos_table[p.lineno(1)-1])
        # Raise the error flag
        self.errFlag = True

    def p_Method(self, p):
        'Method : object_identifier lpar Formals rpar colon Type Block'
        p[0] = Method(p[1], p[3], p[6], p[7])
        p[0].add_position(p.lineno(1), p.lexpos(1) - p.lexer.line_end_pos_table[p.lineno(1)-1])

    # General error rule for method
    def p_Method_error(self, p):
        'Method : object_identifier lpar error rpar colon Type Block'
        error_message_line_col(p.lineno(1), p.lexpos(1) - p.lexer.line_end_pos_table[p.lineno(1)-1], "Something went wrong inside the formals of method " + p[1])
        p[0] = Method(p[1], "", p[6], p[7])
        p[0].add_position(p.lineno(1), p.lexpos(1) - p.lexer.line_end_pos_table[p.lineno(1)-1])
        # Raise the error flag
        self.errFlag = True

    def p_Type(self, p):
        '''Type : type_identifier
                | int32
                | bool
                | string
                | unit'''
        p[0] = Type(p[1])
        p[0].add_position(p.lineno(1), p.lexpos(1) - p.lexer.line_end_pos_table[p.lineno(1)-1])

    def p_Formals(self, p):
        '''Formals :
                   | Formal
                   | Formals comma Formal'''
        if(len(p)==1):
            p[0] = Formals()
            # Empty formals does not have valid position
        elif(len(p)==2):
            p[0] = Formals()
            p[0].add_formal(p[1])
            p[0].add_position_from_node(p[1])
            
        else:
            p[0] = p[1]
            p[0].add_formal(p[3])

    # Error rule for formals when not separated by a comma
    def p_Formals_error_comma(self, p):
        '''Formals : Formals Formal'''
        error_message_node(p[2], "Formals must be separeted by a comma.")
        p[0] = p[1]
        p[0].add_formal(p[2])
        # Raise the error flag
        self.errFlag = True

    def p_Formal(self, p):
        'Formal : object_identifier colon Type'
        p[0] = Formal(p[1], p[3])
        p[0].add_position(p.lineno(1), p.lexpos(1) - p.lexer.line_end_pos_table[p.lineno(1)-1])

        # Error rule for formals when type is not declared
    def p_Formals_error_type(self, p):
        'Formal : object_identifier'
        p[0] = Formal(p[1], "")
        p[0].add_position(p.lineno(1), p.lexpos(1) - p.lexer.line_end_pos_table[p.lineno(1)-1])
        error_message_line_col(p.lineno(1), p.lexpos(1) - p.lexer.line_end_pos_table[p.lineno(1)-1], "Must declare the type of formal " + p[1])    
        # Raise the error flag
        self.errFlag = True

    def p_Block(self, p):
        'Block : lbrace Block_body rbrace'
        p[0] = p[2]

    # General error rule for block
    def p_Block_error(self, p):
        '''Block : lbrace error rbrace'''
        p[0] = Expr_Unit()
        p[0].add_position(p.lineno(1), p.lexpos(1) - p.lexer.line_end_pos_table[p.lineno(1)-1])
        error_message_line_col(p.lineno(1), p.lexpos(1) - p.lexer.line_end_pos_table[p.lineno(1)-1], "Something went wrong inside a block/between braces")
        # Raise the error flag
        self.errFlag = True

    # Error rule for empty block
    def p_Block_error_empty(self, p):
        '''Block : lbrace rbrace'''
        p[0] = Expr_Unit()
        p[0].add_position(p.lineno(1), p.lexpos(1) - p.lexer.line_end_pos_table[p.lineno(1)-1])
        error_message_line_col(p.lineno(1), p.lexpos(1) - p.lexer.line_end_pos_table[p.lineno(1)-1], "A block must not be empty")
        # Raise the error flag
        self.errFlag = True

    # Error rule for detecting block ending with a semicolon
    def p_Block_error_end_semicolon(self, p):
        '''Block : lbrace Block_body semicolon rbrace'''
        p[0] = p[2]
        error_message_line_col(p.lineno(3), p.lexpos(3) - p.lexer.line_end_pos_table[p.lineno(3)-1], "The last expression of a block must NOT end with a semicolon.")
        # Raise the error flag
        self.errFlag = True

    def p_Block_body(self, p):
        '''Block_body : Expr
                      | Block_body semicolon Expr'''
        if(len(p)==2):
            p[0] = Block()
            p[0].add_expr(p[1])
            p[0].add_position_from_node(p[1])
        else:
            p[0] = p[1]
            p[0].add_expr(p[3])
            p[0].add_position_from_node(p[3])

     # Error rule for block body when expression are not separated by semicolon
    def p_Block_body_error_expr_semicolon(self, p):
        '''Block_body : Block_body Expr'''
        p[0] = p[1]
        error_message_node(p[2], "Expressions of a block must be separeted by a semicolon.")
        # Raise the error flag
        self.errFlag = True

    ## Expressions
    def p_Expr_If_then(self, p):
        '''Expr : if Expr then Expr %prec if_then
                | if Expr then Expr else Expr'''
        if(len(p)==7):
            p[0] = Expr_if(p[2], p[4])
            p[0].add_else_expr(p[6])
            p[0].add_position(p.lineno(1), p.lexpos(1) - p.lexer.line_end_pos_table[p.lineno(1)-1])
        else:
            p[0] = Expr_if(p[2], p[4])
            p[0].add_position(p.lineno(1), p.lexpos(1) - p.lexer.line_end_pos_table[p.lineno(1)-1])

    def p_Expr_while(self, p):
        'Expr : while Expr do Expr %prec while_prec'
        p[0] = Expr_while(p[2], p[4])
        p[0].add_position(p.lineno(1), p.lexpos(1) - p.lexer.line_end_pos_table[p.lineno(1)-1])

    def p_Expr_let(self, p):
        '''Expr : let object_identifier colon Type in Expr %prec let_prec
                | let object_identifier colon Type assign Expr in Expr %prec let_prec_assign'''
        if(len(p)==7):
            p[0] = Expr_let(p[2], p[4], p[6])
            p[0].add_position(p.lineno(2), p.lexpos(2) - p.lexer.line_end_pos_table[p.lineno(2)-1])
        else:
            p[0] = Expr_let(p[2], p[4], p[8])
            p[0].add_init_expr(p[6])
            p[0].add_position(p.lineno(2), p.lexpos(2) - p.lexer.line_end_pos_table[p.lineno(2)-1])

    #Error rule for let when type is not declared
    def p_Expr_let_error_type(self, p):
        '''Expr : let object_identifier in Expr
                | let object_identifier assign Expr in Expr '''
        if(len(p)==5):
            p[0] = Expr_let(p[2], "", p[4])
            p[0].add_position(p.lineno(2), p.lexpos(2) - p.lexer.line_end_pos_table[p.lineno(2)-1])
        else:
            p[0] = Expr_let(p[2], "", p[6])
            p[0].add_init_expr(p[4])
            p[0].add_position(p.lineno(2), p.lexpos(2) - p.lexer.line_end_pos_table[p.lineno(2)-1])
        error_message_line_col(p.lineno(1), p.lexpos(1) - p.lexer.line_end_pos_table[p.lineno(1)-1], "Must declare the type of let " + p[2])
        # Raise the error flag
        self.errFlag = True

    def p_Expr_assign(self, p):
        'Expr : object_identifier assign Expr'
        p[0] = Expr_assign(p[1], p[3])
        p[0].add_position(p.lineno(1), p.lexpos(1) - p.lexer.line_end_pos_table[p.lineno(1)-1])

    def p_Expr_uminus(self, p):
        'Expr : minus Expr %prec uminus'
        p[0] = Expr_UnOp(p[1], p[2])
        p[0].add_position(p.lineno(1), p.lexpos(1) - p.lexer.line_end_pos_table[p.lineno(1)-1])

    def p_Expr_UnOp(self, p):
        '''Expr : not Expr
                | isnull Expr'''
        p[0] = Expr_UnOp(p[1], p[2])
        p[0].add_position(p.lineno(1), p.lexpos(1) - p.lexer.line_end_pos_table[p.lineno(1)-1])

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
        #p[0].add_position_from_node(p[1])
        p[0].add_position(p.lineno(2), p.lexpos(2) - p.lexer.line_end_pos_table[p.lineno(2)-1])

    def p_Expr_Call(self, p):
        '''Expr : object_identifier lpar Args rpar
                | Expr dot object_identifier lpar Args rpar'''
        if(len(p)==5):
            p[0] = Expr_Call(p[1], p[3])
            p[0].add_position(p.lineno(1), p.lexpos(1) - p.lexer.line_end_pos_table[p.lineno(1)-1])
        else:
            p[0] = Expr_Call(p[3], p[5])
            p[0].add_object_expr(p[1])
            p[0].add_position_from_node(p[1])
            

    def p_Expr_New(self, p):
        'Expr : new type_identifier'
        p[0] = Expr_New(p[2])
        p[0].add_position(p.lineno(2), p.lexpos(2) - p.lexer.line_end_pos_table[p.lineno(2)-1])

    # Error rule for new when an object identifier is used
    def p_Expr_New_error_obj_id(self, p):
        'Expr : new object_identifier'
        p[0] = Expr_New(p[2])
        p[0].add_position(p.lineno(2), p.lexpos(2) - p.lexer.line_end_pos_table[p.lineno(2)-1])
        error_message_line_col(p.lineno(1), p.lexpos(1) - p.lexer.line_end_pos_table[p.lineno(1)-1], "New must be called on a type identifier, type identifier start with an uppercase letter.")
        # Raise the error flag
        self.errFlag = True

    def p_Expr_Object_id(self, p):
        'Expr : object_identifier'
        p[0] = Expr_Object_identifier(p[1])
        p[0].add_position(p.lineno(1), p.lexpos(1) - p.lexer.line_end_pos_table[p.lineno(1)-1])

    def p_Expr_literal(self, p):
        'Expr : Literal'
        p[0] = p[1]
        p[0].add_position_from_node(p[1])
        
    def p_Expr_Unit(self, p):
        'Expr : lpar rpar'
        p[0] = Expr_Unit()
        p[0].add_position(p.lineno(1), p.lexpos(1) - p.lexer.line_end_pos_table[p.lineno(1)-1])

    def p_Expr_Par_expr(self, p):
        'Expr : lpar Expr rpar'
        p[0] = p[2]
        p[0].add_position(p.lineno(1), p.lexpos(1) - p.lexer.line_end_pos_table[p.lineno(1)-1])

    # General error rule for Par
    def p_Expr_Par_expr_error(self, p):
        'Expr : lpar error rpar'
        p[0] = Expr_Unit()
        p[0].add_position(p.lineno(1), p.lexpos(1) - p.lexer.line_end_pos_table[p.lineno(1)-1])
        error_message_line_col(p.lineno(1), p.lexpos(1) - p.lexer.line_end_pos_table[p.lineno(1)-1], "Something went wrong between/with parentheses")
        # Raise the error flag
        self.errFlag = True

    def p_Expr_block(self,p):
        'Expr : Block'
        p[0] = p[1]
        p[0].add_position_from_node(p[1])

    def p_Args(self, p):
        '''Args :
                | Expr
                | Args comma Expr'''
        if(len(p)==1):
            p[0] = Args()
        elif(len(p)==2):
            p[0] = Args()
            p[0].add_arg(p[1])
            p[0].add_position_from_node(p[1])
        else:
            p[0] = p[1]
            p[0].add_arg(p[3])

    # Literal
    def p_Literal(self, p):
        '''Literal : integer_literal
                   | string_literal
                   | Boolean_literal'''
        p[0] = Literal(p[1])
        if isinstance(p[1], int) or isinstance(p[1], str):
            p[0].add_position(p.lineno(1), p.lexpos(1) - p.lexer.line_end_pos_table[p.lineno(1)-1])
        else:
            p[0].add_position_from_node(p[1])

    def p_Boolean_literal(self, p):
        '''Boolean_literal : true
                           | false'''
        if(p[1]=="true"):
            p[0] = Boolean_literal(True)
            p[0].add_position(p.lineno(1), p.lexpos(1) - p.lexer.line_end_pos_table[p.lineno(1)-1])
        else:
            p[0] = Boolean_literal(False)
            p[0].add_position(p.lineno(1), p.lexpos(1) - p.lexer.line_end_pos_table[p.lineno(1)-1])

    def p_error(self, p):
        if not p:
            error_str = file_name + ":" + str(self.lex.lexer.lineno)
            error_str += ":" + str(self.lex.lexer.lexpos - self.lex.lexer.line_end_pos-1)
            error_str += ": syntax error.\n  "
            error_str += "The parser reached the end of file and detected an error, this is probably due to a missing brace.\n"
            sys.stderr.write(error_str)
        else:
            error_message(p, "An error occured while parsing the following token : " + str(p.value))
        # Raise the error flag
        self.errFlag = True


### Error message functions
# Generate error message
def error_message(token, description):
    error_str = file_name + ":" + str(token.lexer.lineno)
    error_str += ":" + str(token.lexpos - token.lexer.line_end_pos)
    error_str += ": syntax error.\n  " + description + "\n"
    sys.stderr.write(error_str)

# Generate error message
def error_message_node(node, description):
    # Generate the text of the error
    error_str = file_name + ":" + str(node.line)
    error_str += ":" + str(node.col)
    error_str += ": syntax error.\n  " + description + "\n"
    sys.stderr.write(error_str)

# Generate error message for a class
def error_message_line_col(line, col, description):
    # Generate the text of the error
    error_str = file_name + ":" + str(line)
    error_str += ":" + str(col)
    error_str += ": syntax error.\n  " + description + "\n"
    sys.stderr.write(error_str)