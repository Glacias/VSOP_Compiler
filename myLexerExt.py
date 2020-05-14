# -----------------------------------------------------------------------------
# myLexer.py
#
# File responsible for the lexical analysis
# Made by Simon Bernard and Ivan Klapka for the Project 1 : lexical analysis
# University of Liège - Academic year 2019-2020 - INFO0085-1 Compilers course
# -----------------------------------------------------------------------------

import ply.lex as lex
import sys

class MyLexer(object):
    # List of keyword
    keyword = [
        'and',
        'bool',
        'class',
        'do',
        'extends',
        'external',
        'false',
        'in',
        'int32',
        'isnull',
        'let',
        'new',
        'not',
        'or',
        'string',
        'true',
        'unit',
        'if',
        'then',
        'else',
        'while',
        'xor',
    ]

    # List of operators
    operator = {
        '{' : 'lbrace',
        '}' : 'rbrace',
        '(' : 'lpar',
        ')' : 'rpar',
        ':' : 'colon',
        '::' : 'double_colon',
        ';' : 'semicolon',
        ',' : 'comma',
        '+' : 'plus',
        '++' : 'plusplus',
        '-' : 'minus',
        '--' : 'minusminus',
        '*' : 'times',
        '/' : 'div',
        '%' : 'modulo',
        '^' : 'pow',
        '.' : 'dot',
        '=' : 'equal',
        '<' : 'lower',
        '>' : 'larger',
        '<=' : 'lower_equal',
        '>=' : 'larger_equal',
        '<-' : 'assign',
    }

    # List of token names + keyword
    tokens = [
        'integer_literal',
        'type_identifier',
        'object_identifier',
        'string_literal'] + keyword + list(operator.values())


    # Init
    def __init__(self, file):
        global file_name
        file_name = file

    ###  Tokens

    # Single line comment
    def t_singlelinecomment(self, t):
        r'//.*'
        pass

    #  Line numbers and positional information
    def t_newline(self, t):
        r'\n'
        t.lexer.lineno += 1
        t.lexer.line_end_pos = t.lexpos
        t.lexer.line_end_pos_table.append(t.lexpos)

    def t_whitespace(self, t):
        r'[ \t\r\f]'

    #####  Additionnal mode

    # Declare the states/modes of the lexer
    states = (
        ('commentmode','exclusive'),
        ('stringmode','exclusive')
    )

    ####  Comment Mode

    # Match the first (*. Enter commentmode state.
    def t_nestedcomment(self, t):
        r'\(\*'
        t.lexer.comment_start_line = [t.lexer.lineno]   # Record the starting position
        t.lexer.comment_start_column = [(t.lexpos - t.lexer.line_end_pos)]
        t.lexer.level = 1                             # Initial level
        t.lexer.begin('commentmode')                  # Enter 'commentmode' state

    # Rules for the commentmode state
    def t_commentmode_newline(self, t):
        r'\n'
        t.lexer.lineno += 1
        t.lexer.line_end_pos = t.lexpos
        t.lexer.line_end_pos_table.append(t.lexpos)

    def t_commentmode_lnestedcom(self, t):
        r'\(\*'
        t.lexer.comment_start_line.append(t.lexer.lineno)
        t.lexer.comment_start_column.append(t.lexpos - t.lexer.line_end_pos)
        t.lexer.level +=1

    def t_commentmode_rnestedcom(self, t):
        r'\*\)'
        t.lexer.level -=1
        # If end of nested comment, return to initial
        if t.lexer.level == 0:
            t.lexer.begin('INITIAL')

    # For when comment is not closed
    def t_commentmode_eof(self, t):
        error_str = file_name + ":" + str(t.lexer.comment_start_line.pop(t.lexer.level-1))
        error_str += ":" + str(t.lexer.comment_start_column.pop(t.lexer.level-1))
        error_str += ": lexical error\n  Nested comment is not terminated when end-of-file is reached.\n"
        sys.stderr.write(error_str)
        sys.exit(1)

    # For bad characters, we just skip over it
    def t_commentmode_error(self, t):
        t.lexer.skip(1)

    ####  String mode

    def t_stringstart(self, t):
        r'"'
        t.lexer.string_start_line = t.lexer.lineno   # Record the starting position
        t.lexer.string_start_column = t.lexpos - t.lexer.line_end_pos
        t.lexer.stringvalue = "\""
        t.lexer.begin('stringmode')

    def t_stringmode_escaped_char(self, t):
        r'\\(b|t|n|r|\"|\\|(x[0-9a-fA-F][0-9a-fA-F])|\n[ \t]*)'
        # \" => \x22
        if(t.value == '\\"'):
            t.value = '\\x22'
        # \\ => \x5c
        elif(t.value == '\\\\'):
            t.value = '\\x5c'
        # \b => \x08
        elif(t.value == '\\b'):
            t.value = '\\x08'
        # \t => \x09
        elif(t.value == '\\t'):
            t.value = '\\x09'
        # \r => \x0d
        elif(t.value == '\\r'):
            t.value = '\\x0d'
        # if it is the null char ==> error
        elif(t.value == '\\x00'):
            error_message(t, "Null character inside string.")
            sys.exit(1)
        # if escaped hexa char
        elif('x' in t.value):
            asciival = int(t.value[2:], 16)
            # If char printable
            if((asciival >= 32) and (asciival <= 126)):
                t.value = chr(asciival)

        # \n => \x0a and check for \ to a new line
        if(t.value == '\\n'):
            t.value = '\\x0a'
            t.lexer.stringvalue += t.value
        elif("\n" in t.value):
            t.lexer.lineno += 1
            t.lexer.line_end_pos = t.lexpos + 1
            t.lexer.line_end_pos_table.append(t.lexpos+1)
        else:
            t.lexer.stringvalue += t.value

    def t_stringmode_unknown_escaped_char(self, t):
        r'(\\x..)|(\\.)'
        error_message(t, "Unknown escaped char \"" + t.value + "\".")
        sys.exit(1)

    # For when comment is not closed
    def t_stringmode_eof(self, t):
        error_str = file_name + ":" + str(t.lexer.string_start_line)
        error_str += ":" + str(t.lexer.string_start_column)
        error_str += ": lexical error\n  String is not terminated when end-of-file is reached.\n"
        sys.stderr.write(error_str)
        sys.exit(1)

    # End the string
    def t_stringmode_string_literal(self, t):
        r'"'
        t.value = t.lexer.stringvalue + "\""
        t.lexer.begin('INITIAL')
        return t

    # Newline
    def t_stringmode_newline(self, t):
        r'\n'
        error_message(t, "Line feed inside string without proper use of \\.")
        sys.exit(1)

    def t_stringmode_null_char(self, t):
        r'\^@!'
        error_message(t, "Null character inside string.")
        sys.exit(1)

    # Regular char
    def t_stringmode_regular_char(self, t):
        r'.'
        asciival = ord(t.value)
        # If null char => error
        if(asciival == 0):
            error_message(t, "Null character inside string.")
            sys.exit(1)
        # If char printable
        if((asciival >= 32) and (asciival <= 126)):
            t.lexer.stringvalue += t.value
        else:
            hexa_str = str(hex(asciival))
            # Need to add a zero if <16
            if(asciival < 16):
                t.lexer.stringvalue += "\\x0" + hexa_str[2]
            else:
                t.lexer.stringvalue += "\\x" + hexa_str[2:]

    # Skip wrong charac
    def t_stringmode_error(self, t):
        t.lexer.skip(1)

    #### Initial mode

    # Detect error in integer_literal (except incomplete integer_literal "0x")
    def t_integer_literal_err(self, t):
        r'(?!0x)[0-9]+[a-zA-Z_][0-9a-zA-Z_]*|0x[0-9a-fA-F]+[g-zG-Z_][0-9a-zA-Z_]*'
        error_message(t, str(t.value) + " is not a valid integer literal.")
        sys.exit(1)

    # Detect integer_literal
    def t_integer_literal(self, t):
        r'(0x([0-9a-fA-F]+)|0x|[0-9]+)'

        # If value is 0
        if (t.value == "0"):
            t.value = int(0)
        # If empty integer_literal "0x"
        elif(t.value == "0x"):
            error_message(t, str(t.value) + " is not a valid integer literal.")
            sys.exit(1)
        # If hexa
        elif("x" in t.value):
            t.value = int(t.value, 0)
        # If number remove leading 0
        else:
            t.value = int(t.value.lstrip("0"), 0)
        return t

    def t_type_identifier(self, t):
        r'[A-Z][a-zA-Z_0-9]*'
        # Check for keyword words
        if(t.value in self.keyword):
            t.type = t.value
        return t

    def t_object_identifier(self, t):
        r'[a-z][a-zA-Z_0-9]*'
        # Check for keyword words
        if(t.value in self.keyword):
            t.type = t.value
        return t

    def t_operator_long(self, t):
        r'<-|<=|>=|::|\+\+|\-\-'
        t.type = self.operator.get(t.value,'operator')
        return t

    def t_operator(self, t):
        r'[\{\}\(\)<>\.=\:\-;\*\+,/\^%]'
        t.type = self.operator.get(t.value,'operator')
        return t

    #  Error handling
    def t_error(self, t):
        error_message(t, "Invalid character \'" + t.value[0] + "\'.")
        sys.exit(1)

    # Build the lexer
    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

##### General Functions
# Generate error message
def error_message(token, description):
    error_str = file_name + ":" + str(token.lexer.lineno)
    error_str += ":" + str(token.lexpos - token.lexer.line_end_pos)
    error_str += ": lexical error\n  " + description + "\n"
    sys.stderr.write(error_str)
