# -----------------------------------------------------------------------------
# test1.py
#
# A simple test
# -----------------------------------------------------------------------------
from ply.lex import TOKEN
import argparse
import sys

keyword = [
    'and',
    'bool',
    'class',
    'do',
    'extends',
    'false',
    'in',
    'int32',
    'isnull',
    'let',
    'new',
    'not',
    'string',
    'true',
    'unit',
    'if',
    'then',
    'else',
    'while',
]

# List of operators
operator = {
    '{' : 'lbrace',
    '}' : 'rbrace',
    '(' : 'lpar',
    ')' : 'rpar',
    ':' : 'colon',
    ';' : 'semicolon',
    ',' : 'comma',
    '+' : 'plus',
    '-' : 'minus',
    '*' : 'times',
    '/' : 'div',
    '^' : 'pow',
    '.' : 'dot',
    '=' : 'equal',
    '<' : 'lower',
    '<=' : 'lower_equal',
    '<-' : 'assign',
}

# List of token names + keyword
tokens = [
    'lowercase_letter',
    'uppercase_letter',
    'letter',
    'bin_digit',
    'digit',
    'hex_digit',
    'integer_literal_r',
    'integer_literal',
    'whitespace',
    'newline',
    'type_identifier',
    'object_identifier',
    'operator',
    'string_literal',
    'escape_char',
    'escaped_char_r',
    'test'] + keyword + list(operator.values())

###  Tokens
# Whitespace
#t_whitespace = r'[ \t\n\r\f]'

# Literals
#literals = [ '+','-','*','/' ]

# Letters
#t_lowercase_letter = r'[a-z]'
#t_uppercase_letter = r'[A-Z]'
#t_letter = r'(' + t_lowercase_letter + r'|' + t_uppercase_letter + r')'

# Numbers
t_bin_digit = r'[0-1]';
t_digit = r'(' + t_bin_digit + r'|' + r'[2-9]' + r')'
t_hex_digit = r'(' + t_digit + r'|' + r'[a-f]' + r'|' + r'[A-F]' + r')'
t_integer_literal_r = r'(' + r'(' + r'0x' + r'(' + t_hex_digit + r'+' + r')' + r')' + r'|' + r'(' + t_digit + r'+' + r')' + r')'

# Single line comment
def t_singlelinecomment(t):
    r'//.*'
    pass

#  Line numbers and positional information
def t_newline(t):
    r'\n'
    t.lexer.lineno += 1
    t.lexer.line_end_pos = t.lexpos
    return t

def t_whitespace(t):
    r'[ \t\r\f]'
    return t

#####  Additionnal mode
# Declare the states/modes of the lexer
states = (
    ('commentmode','exclusive'),
    ('stringmode','exclusive')
)

####  Comment Mode
# Match the first (*. Enter commentmode state.
def t_nestedcomment(t):
    r'\(\*'
    t.lexer.comment_start_line = t.lexer.lineno   # Record the starting position
    t.lexer.comment_start_column = t.lexpos - t.lexer.line_end_pos
    t.lexer.level = 1                             # Initial level
    t.lexer.begin('commentmode')                  # Enter 'commentmode' state

# Rules for the commentmode state
def t_commentmode_newline(t):
    r'\n'
    t.lexer.lineno += 1
    t.lexer.line_end_pos = t.lexpos

def t_commentmode_lnestedcom(t):
    r'\(\*'
    t.lexer.level +=1

def t_commentmode_rnestedcom(t):
    r'\*\)'
    t.lexer.level -=1

    # If end of nested comment, return to initial
    if t.lexer.level == 0:
        t.lexer.begin('INITIAL')

# For when comment is not closed
def t_commentmode_eof(t):
    error_str = file_name + ":" + str(t.lexer.comment_start_line)
    error_str += ":" + str(t.lexer.comment_start_column)
    error_str += ": lexical error: Multi-line comment is not terminated when end-of-file is reached"
    print(error_str)
    sys.exit(1)

# For bad characters, we just skip over it
def t_commentmode_error(t):
    t.lexer.skip(1)

####  String mode
def t_stringstart(t):
    r'"'
    t.lexer.string_start_line = t.lexer.lineno   # Record the starting position
    t.lexer.string_start_column = t.lexpos - t.lexer.line_end_pos
    t.lexer.stringvalue = "\""
    t.lexer.begin('stringmode')

t_stringmode_escaped_char_r = r'\\' + r'(' + r'b|t|n|r|\"|\\|(x' + t_hex_digit + t_hex_digit + r')|' + r'\n[ \t]*' + r')'

@TOKEN(t_stringmode_escaped_char_r)
def t_stringmode_escaped_char(t):
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
        error_message(t, "Null character inside string")
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
    else:
        t.lexer.stringvalue += t.value

def t_stringmode_unknown_escaped_char(t):
    r'(\\x..)|(\\.)'
    error_message(t, "Unknown escaped char \"" + t.value + "\"")
    sys.exit(1)

# For when comment is not closed
def t_stringmode_eof(t):
    error_str = file_name + ":" + str(t.lexer.string_start_line)
    error_str += ":" + str(t.lexer.string_start_column)
    error_str += ": lexical error: String is not terminated when end-of-file is reached"
    print(error_str)
    sys.exit(1)

# End the string
def t_stringmode_string_literal(t):
    r'"'
    t.value = t.lexer.stringvalue + "\""
    t.lexer.begin('INITIAL')
    return t

# Newline
def t_stringmode_newline(t):
    r'\n'
    error_message(t, "Line feed inside string without proper use of \\")
    sys.exit(1)

def t_stringmode_null_char(t):
    r'\^@!'
    error_message(t, "Null character inside string")
    sys.exit(1)

# Regular char
def t_stringmode_regular_char(t):
    r'.'
    asciival = ord(t.value)
    # If null char => error
    if(asciival == 0):
        error_message(t, "Null character inside string")
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
def t_stringmode_error(t):
    t.lexer.skip(1)

#### Initial mode

@TOKEN(t_integer_literal_r)
def t_integer_literal(t):
    # Get next token without moving lexer state
    next_tok = get_next_token(t)
    # Checking for eof
    if not next_tok:
        return t

    # Checking for next token to be whitespace or operator
    if not (next_tok.type in (["type_identifier", "object_identifier"])) :
        # If 0
        if (t.value == "0"):
            t.value = int(0)
        # If hexa
        elif("x" in t.value):
            t.value = int(t.value, 0)
        # If number remove leading 0
        else:
            t.value = int(t.value.lstrip("0"), 0)
        return t
    else :
        # Print error
        error_message(t, str(t.value) + str(next_tok.value) + " is not a valid integer literal")
        sys.exit(1)

def t_type_identifier(t):
    r'[A-Z][a-zA-Z_0-9]*'
    # Check for keyword words
    if(t.value in keyword):
        t.type = t.value
    return t

def t_object_identifier(t):
    r'[a-z][a-zA-Z_0-9]*'
    # Check for keyword words
    if(t.value in keyword):
        t.type = t.value
    return t

def t_operator_long(t):
    r'<-|<='
    t.type = operator.get(t.value,'operator')
    return t

def t_operator(t):
    r'[\{\}\(\)<\.=\:\-;\*\+,/\^]'
    t.type = operator.get(t.value,'operator')
    return t

###  Error handling
def t_error(t):
    error_message(t, "Invalid character '" + t.value[0] + "'")
    sys.exit(1)


##### General Functions

def error_message(token, description):
    error_str = file_name + ":" + str(token.lexer.lineno)
    error_str += ":" + str(token.lexpos - token.lexer.line_end_pos)
    error_str += ": lexical error: " + description
    print(error_str)

# Get next token without moving forward
def get_next_token(token):
    # Save all variables from lexer
    saved_lexpos = token.lexer.lexpos
    saved_lineno = token.lexer.lineno
    saved_end_pos = token.lexer.line_end_pos

    # Get next token
    next_token = token.lexer.token()

    # Restore variables
    token.lexer.lexpos = saved_lexpos
    token.lexer.lineno = saved_lineno
    token.lexer.line_end_pos = saved_end_pos

    return next_token


##### Build the lexer
import ply.lex as lex
global file_name

if __name__ == '__main__':
    # Parsing arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-lex', help='Path to the input VSOP source code')
    args = parser.parse_args()

    # Check for path
    if not args.lex:
        print("Argument missing : Path to the input VSOP source code")
        sys.exit(1)

    # Create lexer
    lexer = lex.lex()
    lexer.line_end_pos = -1

    # Test it out
    #data = '''
    #a lol 502 +
    #327+
    #(* lololol
    #(*
    #kerk *)
    #" lul \\t"*)
    #0x7
    #"A supposedly very very long str\\
    #ing."
    #"Here comes (* Zorglub *)"
    #"Uninterrupted string // Zorglub"
    #" some thing \\b \\" bool \\r"
    #"\\x66oo\\\\bar\v\\"N M\\"\\n"
    #// hu 12
    #bool
    #someFun42
    #a\te
    #someFun 42
    #0x45
    #0xabcdef gh
    #lol
    #'''

    # Set file_name
    file_name = args.lex.split('\\')[-1:][0]
    if ".vsop" in file_name :
        file_name = file_name[:-5]
    else:
        print("Not a vsop file")

    # Give the lexer some input
    f = open(args.lex, "r")
    data = f.read()
    lexer.input(data)

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            break     # No more input

        # Check for string
        if (tok.type == "string_literal"):
            token_str = str(lexer.string_start_line) + "," + str(lexer.string_start_column) + "," + tok.type.replace("_","-")
            token_str += ("," + str(tok.value))
            print(token_str)

        # Check for string
        elif (tok.type == "type_identifier" or tok.type == "object_identifier" or tok.type == "integer_literal"):
            token_str = str(tok.lineno) + "," + str(tok.lexpos - lexer.line_end_pos) + "," + tok.type.replace("_","-")
            token_str += ("," + str(tok.value))
            print(token_str)

        # Ignore whitespace and newline
        elif not (tok.type == "whitespace" or tok.type == "newline") :
            token_str = str(tok.lineno) + "," + str(tok.lexpos - lexer.line_end_pos) + "," + tok.type.replace("_","-")
            #token_str += ("," + str(tok.value))
            print(token_str)
