# -----------------------------------------------------------------------------
# test1.py
#
# A simple test
# -----------------------------------------------------------------------------
from ply.lex import TOKEN

keyword = {
    'and' : 'AND',
    'bool' : 'BOOL',
    'class' : 'CLASS',
    'do' : 'DO',
    'extends' : 'EXTENDS',
    'false' : 'FALSE',
    'in' : 'IN',
    'int32' : 'INT32',
    'isnull' : 'ISNULL',
    'let' : 'LET',
    'new' : 'NEW',
    'not' : 'NOT',
    'string' : 'STRING',
    'true': 'TRUE',
    'unit' : 'UNIT',
    'if' : 'IF',
    'then' : 'THEN',
    'else' : 'ELSE',
    'while' : 'WHILE',
}

# List of operators
operator = {
    '{' : 'lbrace',
    '}' : 'rbrace',
    '(' : 'lpar',
    ')' : 'rpar',
    ':' : 'colon',
    ';' : 'semicolon',
    ',' : 'coma',
    '+' : 'plus',
    '-' : 'minus',
    '*' : 'times',
    '/' : 'div',
    '^' : 'pow',
    '.' : 'dot',
    '=' : 'equal',
    '<' : 'lower',
    '<=' : 'lower_equal',
    '<-' : 'asign',
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
    'test'] + list(keyword.values()) + list(operator.values())

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
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
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
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
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
    error_str += ": Multi-line comment is not terminated when end-of-file is reached"
    print(error_str)
    exit(1)

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
        exit(1)
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
    elif(t.value.count("\n") != 0):
        t.lexer.lineno += t.value.count("\n")
        t.lexer.line_end_pos = t.lexpos
    else:
        t.lexer.stringvalue += t.value

def t_stringmode_unknown_escaped_char(t):
    r'(\\x..)|(\\.)'
    error_message(t, "Unknown escaped char \"" + t.value + "\"")
    exit(1)

# For when comment is not closed
def t_stringmode_eof(t):
    error_str = file_name + ":" + str(t.lexer.string_start_line)
    error_str += ":" + str(t.lexer.string_start_column)
    error_str += ": String is not terminated when end-of-file is reached"
    print(error_str)
    exit(1)

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
    exit(1)

# Regular char
def t_stringmode_regular_char(t):
    r'.'
    asciival = ord(t.value)
    # If null char => error
    if(asciival == 0):
        error_message(t, "Null character inside string")
        exit(1)
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
        exit(1)

def t_type_identifier(t):
    r'[A-Z][a-zA-Z_0-9]*'
    t.type = keyword.get(t.value,'type_identifier')    # Check for keyword words
    return t

def t_object_identifier(t):
    r'[a-z][a-zA-Z_0-9]*'
    t.type = keyword.get(t.value,'object_identifier')    # Check for keyword words
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
    exit(1)

##### Build the lexer
import ply.lex as lex
lexer = lex.lex()
lexer.line_end_pos = 0

# Test it out
data = '''
a lol 502 +
327+
(* lololol

(*
kerk *)
" lul \\t"*)
0x7
"A supposedly very very long str\\
ing."
"Here comes (* Zorglub *)"
"Uninterrupted string // Zorglub"
" some thing \\b \\" bool \\r"
"\\x66oo\\\\bar\v\\"N M\\"\\n"
// hu 12
bool
someFun42
a\te
someFun 42
0x45
0xabcdef gh
'''

def error_message(token, description):
    error_str = file_name + ":" + str(token.lexer.lineno)
    error_str += ":" + str(token.lexpos - token.lexer.line_end_pos)
    error_str += ": " + description
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

# Give the lexer some input
global file_name
file_name = "FILENAME"
f = open("teacher/05-hex-numbers.vsop", "r")
#data = f.read()
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break     # No more input
    # Check for string
    if (tok.type == "string_literal"):
        token_str = str(lexer.string_start_line) + "," + str(lexer.string_start_column) + "," + str(tok.type)
        #if(tok.type == "hex_digit"):
        token_str += ("," + str(tok.value))
        #TODO
        print(token_str)
    # Ignore whitespace and newline
    elif not (tok.type == "whitespace" or tok.type == "newline") :
        token_str = str(tok.lineno) + "," + str(tok.lexpos - lexer.line_end_pos) + "," + str(tok.type)
        #if(tok.type == "hex_digit"):
        token_str += ("," + str(tok.value))
        #TODO
        print(token_str)
