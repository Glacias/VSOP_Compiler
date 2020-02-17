# -----------------------------------------------------------------------------
# test1.py
#
# A simple test
# -----------------------------------------------------------------------------
from ply.lex import TOKEN

reserved = {
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

# List of token names + reserved
tokens = [
    'lowercase_letter',
    'uppercase_letter',
    'letter',
    'bin_digit',
    'digit',
    'hex_digit',
    'integer_literal_r',
    'integer_literal_r_n',
    'integer_literal',
    'ID',
    'test'] + list(reserved.values())

###  Tokens
# Whitespace
#t_ignore_whitespace = r'[ \t\n\r\f\v]'

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

def t_ignore_whitespace(t):
    r'[ \t\r\f\v]'
    pass

@TOKEN(t_integer_literal_r)
def t_integer_literal(t):
    return t

def t_ID(t):
    r'[a-z][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t



###  Error handling
def t_error(t):
    token_str = file_name + ":" + str(t.lexer.lineno)
    token_str += ":" + str(t.lexpos - t.lexer.line_end_pos)
    token_str += ": Invalid character '" + t.value[0] + "'"
    print(token_str)
    t.lexer.skip(1)


####  Comment Mode
# Declare the state
states = (
    ('commentmode','exclusive'),
)

# Match the first (*. Enter commentmode state.
def t_nestedcomment(t):
    r'\(\*'
    t.lexer.comment_start_line = t.lexer.lineno   # Record the starting position
    t.lexer.comment_start_column = t.lexpos - t.lexer.line_end_pos
    t.lexer.level = 1                             # Initial level
    t.lexer.begin('commentmode')                  # Enter 'commentmode' state

# Rules for the commentmode state
def t_commentmode_lnestedcom(t):
    r'\(\*'
    t.lexer.level +=1

def t_commentmode_rnestedcom(t):
    r'\*\)'
    t.lexer.level -=1

    # If end of nested comment, return to initial
    if t.lexer.level == 0:
        #t.type = "commentmode"
        t.lexer.lineno += t.value.count('\n')
        t.lexer.begin('INITIAL')
        #return t

# Skip any sequence of non-whitespace characters
def t_commentmode_nonspace(t):
    r'[^\s\{\}\'\"]+'
    pass

# Ignored characters (whitespace)
t_commentmode_ignore = " \t\n\r\f\v"

# For bad characters, we just skip over it
def t_commentmode_error(t):
    t.lexer.skip(1)

# For when comment is not closed
def t_commentmode_eof(t):
    token_str = file_name + ":" + str(t.lexer.comment_start_line)
    token_str += ":" + str(t.lexer.comment_start_column)
    token_str += ": Multi-line comment is not terminated when end-of-file is reached"
    print(token_str)


##### Build the lexer
import ply.lex as lex
lexer = lex.lex()
lexer.line_end_pos = 0

# Test it out
data = '''
a lol 502
0x7
//hu 12
someFun42
someFun 42
0x45
0xabcdefgh
and
'''

# Compute column.
#     input is the input text string
#     token is a token instance
def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

# Give the lexer some input
lexer.input(data)
global file_name
file_name = "FILENAME"

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break     # No more input
    token_str = str(tok.lineno) + "," + str(find_column(data,tok)) + "," + str(tok.type)
    #if(tok.type == "hex_digit"):
    token_str += ("," + str(tok.value))
    #TODO
    print(token_str)
